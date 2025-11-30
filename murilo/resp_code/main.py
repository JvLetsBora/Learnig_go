# pico_full_commented.py
# MicroPython code for Raspberry Pi Pico
# Features:
# - ADC reading (GP26 / ADC0)
# - EMA smoothing
# - Map to 0-100
# - USB CDC send "VAL:x.xx"
# - Receive "LED:ON", "LED:OFF", "LED:PWM:val"
# - Single-loop non-blocking architecture
# - Safe fallback if usb_cdc module not present

from machine import ADC, Pin, PWM
import time
import sys

try:
    import usb_cdc
    usb_available = True
    usb = usb_cdc.data  
except Exception:
    usb_available = False
    usb = None


ADC_PIN = 26            # GP26 == ADC0
LED_PIN = 21            # Digital LED control
PWM_PIN = 20            # PWM for LED brightness
SAMPLE_INTERVAL_MS = 50 # sample ADC every 50 ms
SEND_MIN_INTERVAL_MS = 50  # minimal interval between sends
EMA_ALPHA = 0.25        # smoothing factor (0 < alpha <= 1)
CALIB_MIN = 0           # raw ADC min for mapping (set via calibration if needed)
CALIB_MAX = 65535       # raw ADC max for mapping
PWM_FREQ = 1000         # PWM frequency Hz
PWM_MAX = 65535         # PWM duty range for PWM.duty_u16
SEND_ON_CHANGE = True   # only send when value changed by threshold
SEND_CHANGE_THRESHOLD = 0.2  # in mapped units (0-100)

# --- SETUP PERIPHERALS ---
adc = ADC(ADC_PIN)
led_pin = Pin(LED_PIN, Pin.OUT)
pwm = PWM(Pin(PWM_PIN))
pwm.freq(PWM_FREQ)
pwm.duty_u16(0)  # off initially

ema_val = None
last_send_ms = 0
last_sent_mapped = None

rx_buffer = bytearray()

def map_raw_to_0_100(raw):
    
    r = max(CALIB_MIN, min(CALIB_MAX, raw))
    span = CALIB_MAX - CALIB_MIN
    if span == 0:
        return 0.0
    return ( (r - CALIB_MIN) / span ) * 100.0

def safe_write_line(s):
    
    line = s if isinstance(s, bytes) else s.encode()
    if usb_available:
        try:
           
            usb.write(line + b'\n')
        except Exception:
            
            try:
                sys.stdout.write(s + '\n ERROR - usb')
            except Exception:
                pass
    else:
        
        try:
            sys.stdout.write(s + '\n')
        except Exception:
            pass

def handle_command(line):
    line = line.strip()
    if not line:
        return
    parts = line.split(':')
    if parts[0].upper() == 'LED':
        if len(parts) == 2:
            if parts[1].upper() == 'ON':
                led_pin.value(1)
                pwm.duty_u16(0)
            elif parts[1].upper() == 'OFF':
                led_pin.value(0)
                pwm.duty_u16(0)
        elif len(parts) == 3 and parts[1].upper() == 'PWM':
            
            try:
                v = int(parts[2])
                v = max(0, min(255, v))
                
                duty = int((v / 255.0) * PWM_MAX)
                pwm.duty_u16(duty)
                
                led_pin.value(1 if v > 0 else 0)
            except Exception:
                pass

def usb_read_available():
    if not usb_available:
        return b''
    try:
        data = usb.read(64)
        if data:
            return data
    except Exception:
        pass
    return b''

# MAIN LOOP
last_sample_ms = time.ticks_ms()

while True:
    now = time.ticks_ms()

    if time.ticks_diff(now, last_sample_ms) >= SAMPLE_INTERVAL_MS:
        last_sample_ms = now
        raw = adc.read_u16()  # 0..65535
        # EMA smoothing
        if ema_val is None:
            ema_val = float(raw)
        else:
            ema_val = (EMA_ALPHA * raw) + ((1.0 - EMA_ALPHA) * ema_val)

        mapped = map_raw_to_0_100(ema_val)

        # Decide whether to send
        do_send = False
        if last_sent_mapped is None:
            do_send = True
        else:
            if SEND_ON_CHANGE:
                if abs(mapped - last_sent_mapped) >= SEND_CHANGE_THRESHOLD:
                    do_send = True
            else:
                do_send = True

        if do_send and time.ticks_diff(now, last_send_ms) >= SEND_MIN_INTERVAL_MS:
            last_send_ms = now
            last_sent_mapped = mapped
            # format with two decimals
            msg = "VAL:{:.2f}".format(mapped)
            safe_write_line(msg)

    chunk = usb_read_available()
    if chunk:
        # append to rx_buffer and split lines
        rx_buffer.extend(chunk)
        # process full lines
        while True:
            nl = rx_buffer.find(b'\n')
            if nl == -1:
                break
            line = rx_buffer[:nl].decode('utf-8', errors='ignore')
            del rx_buffer[:nl+1]
            handle_command(line)

    time.sleep_ms(1)


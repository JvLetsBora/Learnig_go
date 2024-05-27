import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:http/http.dart' as http;
import 'dart:io';

class ImageUploader extends StatefulWidget {
  const ImageUploader({super.key});

  @override
  State<ImageUploader> createState() => _ImageUploaderState();
}

class _ImageUploaderState extends State<ImageUploader> {
  File? _image;
  final ImagePicker _picker = ImagePicker();
  bool _isLoading = false;
  Image? _processedImage;

  Future<void> _pickImage() async {
    final pickedFile = await _picker.pickImage(source: ImageSource.gallery);

    if (pickedFile != null) {
      setState(() {
        _image = File(pickedFile.path);
        _processedImage = null; // Reset processed image when a new image is picked
      });
    }
  }

  Future<void> _uploadImage() async {
    if (_image == null) return;

    setState(() {
      _isLoading = true;
    });

    final request = http.MultipartRequest(
      'POST',
      Uri.parse('http://172.21.240.1:8000/images/upload/'),
    );
    request.files.add(await http.MultipartFile.fromPath('file', _image!.path));

    final response = await request.send();

    setState(() {
      _isLoading = false;
    });

    if (response.statusCode == 200) {
      final responseData = await response.stream.toBytes();
      setState(() {
        _processedImage = Image.memory(responseData);
      });

      showDialog(
        context: context,
        builder: (_) => AlertDialog(
          title: const Text('Upload successful'),
          content: _processedImage,
          actions: [
            TextButton(
              onPressed: () => Navigator.of(context).pop(),
              child: const Text('OK'),
            ),
          ],
        ),
      );
    } else {
      print('Upload failed with status: ${response.statusCode}');
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Upload failed with status: ${response.statusCode}')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: <Widget>[
            _image != null
                ? Expanded(
                    child: Image.file(
                      _image!,
                      fit: BoxFit.contain,
                      width: double.infinity,
                      height: double.infinity,
                    ),
                  )
                : const Text('No image selected.'),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: _pickImage,
              child: const Text('Select Image'),
            ),
            const SizedBox(height: 20),
            _isLoading
                ? const CircularProgressIndicator()
                : ElevatedButton(
                    onPressed: _uploadImage,
                    child: const Text('Upload Image'),
                  ),
            const SizedBox(height: 20),
            _processedImage != null
                ? Expanded(
                    child: SizedBox(
                      width: double.infinity,
                      height: double.infinity,
                      child: _processedImage,
                    ),
                  )
                : const SizedBox(),
          ],
        ),
      ),
    );
  }
}

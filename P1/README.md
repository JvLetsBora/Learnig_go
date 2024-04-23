# Primeira ponderada


### Comparação com os Princípios REST

1. **Get subjects of a list**
   - Método: GET
   - Descrição: Obtém os assuntos de uma lista.
   - Similaridade com REST: Esta rota segue o princípio de operações baseadas em recursos, onde o recurso "assuntos de uma lista" é acessado através de uma operação GET.

2. **Get editions of a list**
   - Método: GET
   - Descrição: Obtém as edições de uma lista.
   - Similaridade com REST: Assim como a rota anterior, esta também segue o princípio de operações baseadas em recursos ao acessar o recurso "edições de uma lista" através de uma operação GET.

3. **Add a seed from a list**
   - Método: POST
   - Descrição: Adiciona uma semente a partir de uma lista.
   - Similaridade com REST: Esta rota difere dos princípios REST em dois aspectos. Primeiro, ela não segue o princípio de operações baseadas em recursos, pois a ação de adicionar uma semente não é um recurso em si. Em segundo lugar, a rota usa um método POST para uma operação de criação, o que é compatível com REST, mas não necessariamente adere ao conceito de operações REST padrão.

4. **Get seeds of a list**
   - Método: GET
   - Descrição: Obtém as sementes de uma lista.
   - Similaridade com REST: Segue o princípio de operações baseadas em recursos ao acessar o recurso "sementes de uma lista" através de uma operação GET.

5. **Delete a list**
   - Método: POST
   - Descrição: Exclui uma lista.
   - Similaridade com REST: Esta rota também não segue completamente os princípios REST. Embora use um método POST, que pode ser aplicável para operações de exclusão em REST, a ação de exclusão de uma lista não é tratada como um recurso separado. Além disso, o uso de um método POST para uma operação de exclusão é menos comum em REST, que geralmente utiliza o método DELETE para essa finalidade.

6. **Read a list**
   - Método: GET
   - Descrição: Lê uma lista.
   - Similaridade com REST: Segue o princípio de operações baseadas em recursos ao acessar o recurso "lista" através de uma operação GET.

7. **New Request**
   - Método: POST
   - Descrição: Cria uma nova lista.
   - Similaridade com REST: Esta rota segue parcialmente os princípios REST ao usar um método POST para uma operação de criação. No entanto, a estrutura da solicitação, incluindo o envio de texto livre no corpo, pode não ser totalmente alinhada com as práticas REST recomendadas.

8. **Create a list**
   - Método: POST
   - Descrição: Cria uma lista.
   - Similaridade com REST: Similar à rota anterior, esta rota também usa um método POST para uma operação de criação. No entanto, a estrutura da solicitação, incluindo o envio de texto livre no corpo, pode não ser totalmente alinhada com as práticas REST recomendadas.

9. **Search lists**
   - Método: GET
   - Descrição: Pesquisa listas.
   - Similaridade com REST: Segue o princípio de operações baseadas em recursos ao acessar o recurso "listas" através de uma operação GET.

10. **Get a users lists**
    - Método: GET
    - Descrição: Obtém as listas de um usuário.
    - Similaridade com REST: Segue o princípio de operações baseadas em recursos ao acessar o recurso "listas de um usuário" através de uma operação GET.

Essas rotas exibem uma mistura de conformidade e não conformidade com os princípios REST, com algumas rotas seguindo mais de perto os padrões RESTful do que outras. Em particular, as operações de leitura (GET) das listas e seus elementos estão mais alinhadas com os princípios REST, enquanto as operações de criação e exclusão (POST) poderiam ser ajustadas para seguir mais de perto as convenções RESTful.


import datetime
class Cliente:
    def __init__(self, nome, telefone,email,id):
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.id = id
    def __repr__(self):
        return f'Senhor(a) {self.nome}, número de contato {self.telefone}'        
class Quarto:
    def __init__(self, nro_quarto,tipo_quarto,preco_diaria,):
        self.nro_quarto = nro_quarto
        self.tipo_quarto = tipo_quarto
        self.preco_diaria = preco_diaria
        self.disponibilidade = True
    def __repr__(self): #Essa função serve de controle pra você
        return f'número {self.nro_quarto}, Tipo: {self.tipo_quarto}, valor: R${self.preco_diaria:.2f}, Status: {'Disponível'if self.disponibilidade else 'Ocupado'} '
        #Esse retorno possui um if no final que identifica o estado de ocupação do quarto
        
class Reserva:
    def __init__(self,cliente,quarto_reservado,data_checkin,data_checkout):
        if not quarto_reservado.disponibilidade:
            raise ValueError(f"O quarto {quarto_reservado.nro_quarto} não está disponível para reserva.")
        
        self.cliente = cliente #Esse atributo precisa receber um objeto de tipo cliente
        self.quarto = quarto_reservado
        self.data_chekin = data_checkin
        self.data_chekout = data_checkout
        self.status_reserva = 'Confirmada'
        self.quarto.disponibilidade = False #Se Tenho a confirmação que o quarto está desocupado, chegou a hora definir sua disponibilidade como ocupado
        self.id = 0 #Ao decorrer do sistema percebi a necessidade de inserir um id para o reconhecimento da reserva
    def __repr__(self):
        return f'Reserva realizada pelo cliente {self.cliente}, o quarto reservardo foi o {self.quarto}'#o self.quarto possui um retorno personalizado com todos os dados do objeto quarto

    """
    Dono da Reserva
    Quarto Reservado
    Data de check-in  e check-out
    Status da reserva
    """
class GerenciadorDeReservas:
    
    def __init__(self,quartos):
        self.quartos = quartos
        self.reservas = []
    def verificar_disponibilidade_geral(self): #A função desse método é listar todos os quartos cadastrados no sistema, independente da sua disponibilidade
        print("--- Status de Disponibilidade dos Quartos ---")
        if not self.quartos: # Primeiramente ele verificar se algum quarto já foi cadastrado no sistema
            print("Nenhum quarto cadastrado no sistema.")
            return
        for quarto in self.quartos:
            print(quarto) # Sempre quando um objeto de tipo quarto for chamado, ele retornará o _repr_ da classe
        print("-------------------------------------------")


    def listar_quartos_disponiveis(self): #Esse método não possui uma função aplicável ao sistema, apenas parece ser útil para o ambiente de desenvolvimento
        return [quarto.nro_quarto for quarto in self.quartos if quarto.disponibilidade] #Retorna uma lista com o número dos quartos disponíveis

    
    def criar_reserva(self, cliente, data_checkin, data_checkout, nro_quarto): # Essa Função cria uma nova reserva para um cliente em um quarto específico.
        quarto_selecionado = None
        # Começaremos pela procura de um quarto pelo número que foi fornecido
        for quarto in self.quartos:
            if quarto.nro_quarto == nro_quarto:
                quarto_selecionado = quarto
                break
        
        if not quarto_selecionado: #Se o número não estiver listado na nossa lista de quartos as reserva é interrompida
            print(f"Erro: O quarto número {nro_quarto} não existe.")
            return

        try:
            nova_reserva = Reserva(cliente, quarto_selecionado, data_checkin, data_checkout)
            if not self.reservas:
                nova_reserva.id = 1001
            else:
                nova_reserva.id = self.reservas[-1].id+1
        
            self.reservas.append(nova_reserva)
        except ValueError as e:
            # Captura o erro levantado pela classe Reserva se o quarto não estiver disponível
            print(f"Erro ao criar reserva: {e}")
    
    def listar_reservas(self):
       
        print("\n--- Lista de Todas as Reservas Ativas ---")
        if not self.reservas: #Caso a lista esteja vazia
            print("Nenhuma reserva ativa no momento.")
        else:
            for i, reserva in enumerate(self.reservas):
                print(f"{i+1}: {reserva}") # Usa o __repr__ da classe Reserva
        print("-----------------------------------------")
        
    def encontrar_reserva(self, id_reserva):
        for reserva in self.reservas: #Busca uma reserva por meio do id do cliente
            if reserva.id == id_reserva: #sua função não serve apenas para print, mas também possui funções de pesquisa dentro do código
                return reserva
        return None # Retorna None se não encontrar
    def modificar_reserva(self,id_cliente, nova_data_checkout = None, novo_nro_quarto = None): #PENDENTE COMENTAR AS COISAS AQUI
        reserva = self.encontrar_reserva(id_cliente)
        if not reserva:
            print(f"Erro: Nenhuma reserva encontrada para esse id {id_cliente}.")
            return
        if nova_data_checkout:
            reserva.data_checkout = nova_data_checkout
            print(f"Data de check-out da reserva de {reserva.cliente.nome} atualizada para {nova_data_checkout}.")

        if novo_nro_quarto:
            # Verifica se o novo quarto desejado existe e está disponível
            novo_quarto = None
            for q in self.quartos:
                if q.nro_quarto == novo_nro_quarto:
                    novo_quarto = q
                    break
            
            if not novo_quarto:
                print(f"Erro: O quarto {novo_nro_quarto} não existe.")
                return
                
            if not novo_quarto.disponibilidade:
                print(f"Erro: O quarto {novo_nro_quarto} não está disponível para troca.")
                return

            # Libera o quarto antigo e ocupa o novo
            reserva.quarto.disponibilidade = True
            novo_quarto.disponibilidade = False
            reserva.quarto = novo_quarto
            print(f"Quarto da reserva de {reserva.cliente.nome} alterado para {novo_nro_quarto}.")
        
    def cancelar_reserva(self, id_reserva):
        """Cancela uma reserva e torna o quarto disponível novamente."""
        reserva_para_cancelar = self.encontrar_reserva(id_reserva)
        
        if not reserva_para_cancelar:
            print(f"Erro: Nenhuma reserva encontrada para o id {id_reserva}.")
            return
            
        # 1. Torna o quarto disponível novamente
        reserva_para_cancelar.quarto.disponibilidade = True
        
        # 2. Remove a reserva da lista de reservas
        self.reservas.remove(reserva_para_cancelar)
        
        print(f"Reserva em nome de {reserva_para_cancelar.cliente.nome} foi cancelada com sucesso.")


#Criação de quartos para o banco de dados interno do projeto
quarto_101 = Quarto(nro_quarto=101, tipo_quarto="Single", preco_diaria=150.00)
quarto_102 = Quarto(nro_quarto=102, tipo_quarto="Single", preco_diaria=165.00)
quarto_103 = Quarto(nro_quarto=103, tipo_quarto="Single", preco_diaria=155.00)
quarto_205 = Quarto(nro_quarto=205, tipo_quarto="Double", preco_diaria=250.50)
quarto_206 = Quarto(nro_quarto=206, tipo_quarto="Double", preco_diaria=275.00)
quarto_301_suite = Quarto(nro_quarto=301, tipo_quarto="Suite", preco_diaria=450.00)
quarto_302_suite = Quarto(nro_quarto=302, tipo_quarto="Suite", preco_diaria=480.00)
lista_de_quartos = [
    quarto_101, quarto_102, quarto_103, quarto_205, quarto_206,
    quarto_301_suite, quarto_302_suite,
]

#Criação de clientes para o banco de dados interno do projeto
cliente1 = Cliente(nome="Carlos Andrade", telefone="7198877-6655", email="carlos.a@email.com", id=1)
cliente2 = Cliente(nome="Beatriz Lima", telefone="7199988-5544", email="beatriz.lima@email.com", id=2)
cliente3 = Cliente(nome="Daniel Sampaio", telefone="7198123-4567", email="dani.sampaio@email.com", id=3)
cliente4 = Cliente(nome="Fernanda Costa", telefone="7199234-5678", email="fer.costa@email.com", id=4)
cliente5 = Cliente(nome="Juliana Martins", telefone="7198765-4321", email="ju.martins@email.com", id=5)
cliente6 = Cliente(nome="Ricardo Oliveira", telefone="7198234-9876", email="ricardo.o@email.com", id=6)
cliente7 = Cliente(nome="Patricia Souza", telefone="7199345-6789", email="patricia.s@email.com", id=7)
cliente8 = Cliente(nome="Lucas Ferreira", telefone="7198456-7890", email="lucas.f@email.com", id=8)
lista_de_clientes = [
    cliente1, cliente2, cliente3, cliente4,
    cliente5, cliente6, cliente7, cliente8
]

#Criação de um gerenciador de Reservas
gerenciador = GerenciadorDeReservas(lista_de_quartos)

#Criação de Reservas para o banco de dados iterno do projeto
gerenciador.criar_reserva(cliente1,datetime.date(2025, 11, 10),datetime.date(2025, 11, 15),101)
gerenciador.criar_reserva(cliente2,datetime.date(2025, 11, 10),datetime.date(2025, 11, 15),301)



gerenciador.verificar_disponibilidade_geral()
print('Número de Quartos disponíveis: ')
print(gerenciador.listar_quartos_disponiveis())


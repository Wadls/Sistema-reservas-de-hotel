import flet as ft

# Importa as funções que criam cada View (note: não chamamos as funções aqui, só importamos)
from views.home_view import create_home_view
from views.reservation_form_view import create_reservation_form_view
from views.reservations_view import create_reservations_view
from views.clients_view import create_clients_view, create_edit_client_view


def main(page: ft.Page):
    page.title = "Sistema de Reservas Hoteleiras"
    page.theme_mode = ft.ThemeMode.DARK  # Ou LIGHT

    # Dicionário de rotas para fábricas (funções que geram a view quando chamadas)
    routes = {
        "/": create_home_view,
        "/reservar": create_reservation_form_view,
        "/reservas": create_reservations_view,
        "/clientes": create_clients_view,
        # NOTA: rota de edição é tratada separadamente (porque precisa do ID)
    }

    def route_change(route):
        """Chamado quando a rota muda — aqui criamos a view dinamicamente."""
        page.views.clear()

        # rota de edição com parâmetro: /editar_cliente/<id>
        if page.route.startswith("/editar_cliente/"):
            try:
                cliente_id = int(page.route.split("/")[-1])
            except Exception:
                cliente_id = None

            if cliente_id is not None:
                page.views.append(create_edit_client_view(page, cliente_id))
            else:
                # rota inválida: volta para home ou mostra mensagem simples
                page.views.append(create_home_view(page))

        else:
            # rotas normais (chamamos a fábrica passando a page)
            factory = routes.get(page.route, create_home_view)
            page.views.append(factory(page))

        page.update()

    def view_pop(view):
        """Chamado ao fechar uma view (botão voltar) — mantém histórico simples."""
        if page.views:
            page.views.pop()
        # volta para a última view do stack, se houver
        if page.views:
            top_view = page.views[-1]
            page.go(top_view.route)
        else:
            page.go("/")

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    # inicia a rota (se já houver uma route definida por URL, usa ela; caso contrário "/")
    if not page.route or page.route == "/":
        page.go("/")
    else:
        page.go(page.route)


if __name__ == "__main__":
    ft.app(target=main)

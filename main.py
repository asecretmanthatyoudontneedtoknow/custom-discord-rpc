import flet as ft
from pypresence import Presence

def main(page: ft.Page):
    page.title = "Discord RPC Maker"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 450
    page.window_height = 600
    page.theme_mode = ft.ThemeMode.DARK
    
    page.theme = ft.Theme(color_scheme_seed=ft.colors.INDIGO)
    page.padding = 30

    rpc_holder = {"rpc": None}

    def start_rpc(e):
        client_id = client_id_field.value
        state_txt = state_field.value
        details_txt = details_field.value
        large_image = image_field.value

        if not client_id:
            status_text.value = "Error: Client ID is required!"
            status_text.color = ft.colors.ERROR
            page.update()
            return

        try:
            if rpc_holder["rpc"]:
                rpc_holder["rpc"].close()

            rpc = Presence(client_id)
            rpc.connect()
            rpc_holder["rpc"] = rpc

            kwargs = {
                "state": state_txt if state_txt else None,
                "details": details_txt if details_txt else None,
                "large_image": large_image if large_image else None
            }
            rpc.update(**kwargs)

            status_text.value = "Active: RPC is running on Discord!"
            status_text.color = ft.colors.GREEN_400
            
            client_id_field.disabled = True
            btn_start.disabled = True
            btn_stop.disabled = False
            
        except Exception as ex:
            status_text.value = f"Connection Failed: {ex}"
            status_text.color = ft.colors.ERROR
        
        page.update()

    def stop_rpc(e):
        if rpc_holder["rpc"]:
            rpc_holder["rpc"].close()
            rpc_holder["rpc"] = None
        
        status_text.value = "Stopped."
        status_text.color = ft.colors.GREY_400
        client_id_field.disabled = False
        btn_start.disabled = False
        btn_stop.disabled = True
        page.update()

    title_text = ft.Text("RPC Customizer", style=ft.TextThemeStyle.HEADLINE_MEDIUM, weight=ft.FontWeight.BOLD)
    subtitle = ft.Text("Material 3 Edition", style=ft.TextThemeStyle.LABEL_LARGE, color=ft.colors.PRIMARY)

    client_id_field = ft.TextField(label="Client ID", hint_text="Paste from Discord Dev Portal", prefix_icon=ft.icons.ID_CARD_OUTLINED)
    details_field = ft.TextField(label="Details (Row 1)", hint_text="e.g. In the Lobby", prefix_icon=ft.icons.DESCRIPTION_OUTLINED)
    state_field = ft.TextField(label="State (Row 2)", hint_text="e.g. Level 50", prefix_icon=ft.icons.GAMEPAD_OUTLINED)
    image_field = ft.TextField(label="Image Key", hint_text="Art Asset Name", prefix_icon=ft.icons.IMAGE_OUTLINED)

    status_text = ft.Text("Waiting to start...", size=14, color=ft.colors.GREY)

    btn_start = ft.FilledButton(text="Launch RPC", icon=ft.icons.PLAY_ARROW, on_click=start_rpc, width=150)
    btn_stop = ft.FilledTonalButton(text="Stop", icon=ft.icons.STOP, on_click=stop_rpc, width=150, disabled=True)

    main_column

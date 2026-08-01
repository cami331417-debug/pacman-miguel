import os
import sys
import pygame

# 1. INICIALIZACIÓN DE PYGAME Y SISTEMA DE AUDIO
pygame.init()
pygame.mixer.init()

# Configuración de Pantalla Completa Adaptable
info = pygame.display.Info()
ANCHO, ALTO = info.current_w, info.current_h
pantalla = pygame.display.set_mode((ANCHO, ALTO), pygame.FULLSCREEN)
pygame.display.set_caption("PACMAN DE MIGUEL")
reloj = pygame.time.Clock()

# --- CARGAR MÚSICA DE FONDO ---
NOMBRE_CANCION = "musica.mp3"
volumen_musica = 0.5  # Volumen al 50% por defecto

if os.path.exists(NOMBRE_CANCION):
    pygame.mixer.music.load(NOMBRE_CANCION)
    pygame.mixer.music.set_volume(volumen_musica)
    pygame.mixer.music.play(-1)
else:
    print(
        f"Aviso: Guarda el archivo '{NOMBRE_CANCION}' en la misma carpeta para escuchar la música."
    )

# 2. PALETA DE COLORES
NEGRO = (0, 0, 0)
AMARILLO = (255, 255, 0)
BLANCO = (255, 255, 255)
GRIS = (60, 60, 60)
VERDE = (0, 200, 0)
AZUL = (0, 100, 255)
ROJO = (220, 20, 60)
DORADO = (255, 215, 0)
AZUL_OSCURO = (15, 15, 35)
AZUL_PARED = (25, 25, 112)

# 3. ESTADO DEL JUEGO Y VARIABLES GLOBALES
estado = "MENU"  # Estados: MENU, DIFICULTAD, TIENDA_ROPA, TIENDA_MONEDAS, JUEGO, PAUSA
monedas = 100
velocidad_fantasma = 2

# 4. FUENTES TIPOGRÁFICAS DINÁMICAS
f_titulo = pygame.font.SysFont("arial", int(ANCHO * 0.05), bold=True)
f_sub = pygame.font.SysFont("arial", int(ANCHO * 0.03), bold=True)
f_btn = pygame.font.SysFont("arial", int(ANCHO * 0.022), bold=True)

# 5. LABERINTOS SEGÚN DIFICULTAD (1 = Pared, 0 = Camino)
MAPA_FACIL = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

MAPA_INTERMEDIO = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

MAPA_DIFICIL = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

mapa_actual = MAPA_FACIL

# 6. DEFINICIÓN DE BOTONES E INTERFAZ
tam_ic = int(ANCHO * 0.12)
c_y = int(ALTO * 0.55)

# Menú Principal
btn_play = pygame.Rect(ANCHO // 2 - int(tam_ic * 1.8), c_y, tam_ic, tam_ic)
btn_ropa = pygame.Rect(ANCHO // 2 - tam_ic // 2, c_y, tam_ic, tam_ic)
btn_banco = pygame.Rect(ANCHO // 2 + int(tam_ic * 0.8), c_y, tam_ic, tam_ic)

# Selector de Dificultad
w_dif, h_dif = int(ANCHO * 0.35), int(ALTO * 0.1)
btn_facil = pygame.Rect(ANCHO // 2 - w_dif // 2, int(ALTO * 0.35), w_dif, h_dif)
btn_inter = pygame.Rect(ANCHO // 2 - w_dif // 2, int(ALTO * 0.50), w_dif, h_dif)
btn_dificil = pygame.Rect(
    ANCHO // 2 - w_dif // 2, int(ALTO * 0.65), w_dif, h_dif
)

btn_volver = pygame.Rect(
    int(ANCHO * 0.03), int(ALTO * 0.03), int(ANCHO * 0.12), int(ALTO * 0.07)
)
btn_pausa_in_game = pygame.Rect(
    int(ANCHO * 0.85), int(ALTO * 0.03), int(ANCHO * 0.12), int(ALTO * 0.07)
)

# Menú de Pausa (Estilo Geometry Dash)
w_pau, h_pau = int(ANCHO * 0.35), int(ALTO * 0.08)
btn_reanudar = pygame.Rect(
    ANCHO // 2 - w_pau // 2, int(ALTO * 0.30), w_pau, h_pau
)
btn_reiniciar = pygame.Rect(
    ANCHO // 2 - w_pau // 2, int(ALTO * 0.42), w_pau, h_pau
)

# Control de Volumen
btn_vol_menos = pygame.Rect(
    ANCHO // 2 - int(w_pau * 0.48), int(ALTO * 0.54), int(w_pau * 0.25), h_pau
)
btn_vol_mas = pygame.Rect(
    ANCHO // 2 + int(w_pau * 0.23), int(ALTO * 0.54), int(w_pau * 0.25), h_pau
)

btn_salir_menu = pygame.Rect(
    ANCHO // 2 - w_pau // 2, int(ALTO * 0.68), w_pau, h_pau
)


def dibujar_mapa(matriz):
    filas = len(matriz)
    columnas = len(matriz[0])
    tam_bloque = min(
        int(ANCHO * 0.8) // columnas, int(ALTO * 0.7) // filas
    )
    offset_x = (ANCHO - (columnas * tam_bloque)) // 2
    offset_y = (ALTO - (filas * tam_bloque)) // 2 + 30

    for f in range(filas):
        for c in range(columnas):
            if matriz[f][c] == 1:
                rect_pared = pygame.Rect(
                    offset_x + c * tam_bloque,
                    offset_y + f * tam_bloque,
                    tam_bloque,
                    tam_bloque,
                )
                pygame.draw.rect(pantalla, AZUL_PARED, rect_pared)
                pygame.draw.rect(
                    pantalla, AZUL, rect_pared, width=2, border_radius=4
                )


# 7. BUCLE PRINCIPAL DEL JUEGO
corriendo = True
while corriendo:
    pantalla.fill(AZUL_OSCURO)
    pos_mouse = pygame.mouse.get_pos()
    clic = False

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        if evento.type == pygame.MOUSEBUTTONDOWN:
            clic = True
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                if estado == "JUEGO":
                    estado = "PAUSA"
                elif estado == "PAUSA":
                    estado = "JUEGO"
                elif estado != "MENU":
                    estado = "MENU"

    # --- PANTALLA: MENÚ PRINCIPAL ---
    if estado == "MENU":
        txt_t = f_titulo.render("PACMAN DE MIGUEL", True, AMARILLO)
        txt_m = f_sub.render(f"Monedas: ${monedas}", True, DORADO)
        pantalla.blit(txt_t, (ANCHO // 2 - txt_t.get_width() // 2, ALTO * 0.18))
        pantalla.blit(txt_m, (ANCHO // 2 - txt_m.get_width() // 2, ALTO * 0.32))

        txt_musi = f_btn.render("🎵 Música: Shape of You", True, VERDE)
        pantalla.blit(
            txt_musi, (ANCHO // 2 - txt_musi.get_width() // 2, ALTO * 0.85)
        )

        col_p = AMARILLO if btn_play.collidepoint(pos_mouse) else VERDE
        pygame.draw.rect(pantalla, col_p, btn_play, border_radius=20)

        col_r = AMARILLO if btn_ropa.collidepoint(pos_mouse) else AZUL
        pygame.draw.rect(pantalla, col_r, btn_ropa, border_radius=20)

        col_b = AMARILLO if btn_banco.collidepoint(pos_mouse) else DORADO
        pygame.draw.rect(pantalla, col_b, btn_banco, border_radius=20)

        if clic:
            if btn_play.collidepoint(pos_mouse):
                estado = "DIFICULTAD"
            if btn_ropa.collidepoint(pos_mouse):
                estado = "TIENDA_ROPA"
            if btn_banco.collidepoint(pos_mouse):
                estado = "TIENDA_MONEDAS"

    # --- PANTALLA: SELECTOR DE DIFICULTAD ---
    elif estado == "DIFICULTAD":
        txt_d = f_titulo.render("SELECCIONA DIFICULTAD", True, BLANCO)
        pantalla.blit(txt_d, (ANCHO // 2 - txt_d.get_width() // 2, ALTO * 0.15))

        pygame.draw.rect(pantalla, GRIS, btn_volver, border_radius=10)
        t_v = f_btn.render("VOLVER", True, BLANCO)
        pantalla.blit(
            t_v,
            (
                btn_volver.x + (btn_volver.width - t_v.get_width()) // 2,
                btn_volver.y + (btn_volver.height - t_v.get_height()) // 2,
            ),
        )
        if clic and btn_volver.collidepoint(pos_mouse):
            estado = "MENU"

        niveles = [
            (btn_facil, "FÁCIL (Mapa Abierto)", VERDE, 2, MAPA_FACIL),
            (btn_inter, "INTERMEDIO (Laberinto)", DORADO, 4, MAPA_INTERMEDIO),
            (btn_dificil, "DIFÍCIL (Pasillos Estrechos)", ROJO, 7, MAPA_DIFICIL),
        ]

        for btn, texto, col, vel, mapa in niveles:
            col_act = AMARILLO if btn.collidepoint(pos_mouse) else col
            pygame.draw.rect(pantalla, col_act, btn, border_radius=15)
            t_txt = f_btn.render(texto, True, NEGRO)
            pantalla.blit(
                t_txt,
                (
                    btn.x + (btn.width - t_txt.get_width()) // 2,
                    btn.y + (btn.height - t_txt.get_height()) // 2,
                ),
            )

            if clic and btn.collidepoint(pos_mouse):
                velocidad_fantasma = vel
                mapa_actual = mapa
                estado = "JUEGO"

    # --- PANTALLAS: TIENDAS ---
    elif estado in ["TIENDA_ROPA", "TIENDA_MONEDAS"]:
        titulo_tienda = (
            "TIENDA DE SKINS"
            if estado == "TIENDA_ROPA"
            else "BANCO DE MONEDAS"
        )
        txt_t = f_titulo.render(titulo_tienda, True, BLANCO)
        pantalla.blit(txt_t, (ANCHO // 2 - txt_t.get_width() // 2, ALTO * 0.2))

        pygame.draw.rect(pantalla, GRIS, btn_volver, border_radius=10)
        t_v = f_btn.render("VOLVER", True, BLANCO)
        pantalla.blit(
            t_v,
            (
                btn_volver.x + (btn_volver.width - t_v.get_width()) // 2,
                btn_volver.y + (btn_volver.height - t_v.get_height()) // 2,
            ),
        )
        if clic and btn_volver.collidepoint(pos_mouse):
            estado = "MENU"

    # --- PANTALLA: MODO DE JUEGO Y MENÚ DE PAUSA ---
    elif estado in ["JUEGO", "PAUSA"]:
        pantalla.fill(NEGRO)
        txt_j = f_sub.render("JUGANDO PACMAN DE MIGUEL", True, BLANCO)
        pantalla.blit(txt_j, (20, 20))

        dibujar_mapa(mapa_actual)

        # Botón de Pausa en la esquina
        pygame.draw.rect(pantalla, GRIS, btn_pausa_in_game, border_radius=10)
        t_pau = f_btn.render("PAUSA ⏸", True, BLANCO)
        pantalla.blit(
            t_pau,
            (
                btn_pausa_in_game.x
                + (btn_pausa_in_game.width - t_pau.get_width()) // 2,
                btn_pausa_in_game.y
                + (btn_pausa_in_game.height - t_pau.get_height()) // 2,
            ),
        )

        if clic and btn_pausa_in_game.collidepoint(pos_mouse):
            estado = "PAUSA"

        # Ventana de Pausa
        if estado == "PAUSA":
            capa_oscura = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            capa_oscura.fill((0, 0, 0, 180))
            pantalla.blit(capa_oscura, (0, 0))

            txt_pausa_tit = f_titulo.render("JUEGO EN PAUSA", True, AMARILLO)
            pantalla.blit(
                txt_pausa_tit,
                (ANCHO // 2 - txt_pausa_tit.get_width() // 2, ALTO * 0.15),
            )

            # Botones del menú de pausa
            col_rea = (
                AMARILLO if btn_reanudar.collidepoint(pos_mouse) else VERDE
            )
            pygame.draw.rect(pantalla, col_rea, btn_reanudar, border_radius=12)
            t_rea = f_btn.render("▶ REANUDAR", True, NEGRO)
            pantalla.blit(
                t_rea,
                (
                    btn_reanudar.x
                    + (btn_reanudar.width - t_rea.get_width()) // 2,
                    btn_reanudar.y
                    + (btn_reanudar.height - t_rea.get_height()) // 2,
                ),
            )

            col_rei = (
                AMARILLO if btn_reiniciar.collidepoint(pos_mouse) else DORADO
            )
            pygame.draw.rect(
                pantalla, col_rei, btn_reiniciar, border_radius=12
            )
            t_rei = f_btn.render("🔄 REINICIAR PARTIDA", True, NEGRO)
            pantalla.blit(
                t_rei,
                (
                    btn_reiniciar.x
                    + (btn_reiniciar.width - t_rei.get_width()) // 2,
                    btn_reiniciar.y
                    + (btn_reiniciar.height - t_rei.get_height()) // 2,
                ),
            )

            # Volumen
            pygame.draw.rect(pantalla, AZUL, btn_vol_menos, border_radius=10)
            t_vol_m = f_btn.render("- VOL", True, BLANCO)
            pantalla.blit(
                t_vol_m,
                (
                    btn_vol_menos.x
                    + (btn_vol_menos.width - t_vol_m.get_width()) // 2,
                    btn_vol_menos.y
                    + (btn_vol_menos.height - t_vol_m.get_height()) // 2,
                ),
            )

            porcentaje_vol = int(volumen_musica * 100)
            t_vol_txt = f_btn.render(
                f"🔊 {porcentaje_vol}%", True, BLANCO
            )
            pantalla.blit(
                t_vol_txt,
                (ANCHO // 2 - t_vol_txt.get_width() // 2, int(ALTO * 0.56)),
            )

            pygame.draw.rect(pantalla, AZUL, btn_vol_mas, border_radius=10)
            t_vol_p = f_btn.render("+ VOL", True, BLANCO)
            pantalla.blit(
                t_vol_p,
                (
                    btn_vol_mas.x
                    + (btn_vol_mas.width - t_vol_p.get_width()) // 2,
                    btn_vol_mas.y
                    + (btn_vol_mas.height - t_vol_p.get_height()) // 2,
                ),
            )

            col_sal = (
                AMARILLO if btn_salir_menu.collidepoint(pos_mouse) else ROJO
            )
            pygame.draw.rect(
                pantalla, col_sal, btn_salir_menu, border_radius=12
            )
            t_sal = f_btn.render("🚪 SALIR AL MENÚ", True, BLANCO)
            pantalla.blit(
                t_sal,
                (
                    btn_salir_menu.x
                    + (btn_salir_menu.width - t_sal.get_width()) // 2,
                    btn_salir_menu.y
                    + (btn_salir_menu.height - t_sal.get_height()) // 2,
                ),
            )

            if clic:
                if btn_reanudar.collidepoint(pos_mouse):
                    estado = "JUEGO"
                if btn_reiniciar.collidepoint(pos_mouse):
                    estado = "JUEGO"
                if btn_vol_menos.collidepoint(pos_mouse):
                    volumen_musica = max(0.0, volumen_musica - 0.1)
                    pygame.mixer.music.set_volume(volumen_musica)
                if btn_vol_mas.collidepoint(pos_mouse):
                    volumen_musica = min(1.0, volumen_musica + 0.1)
                    pygame.mixer.music.set_volume(volumen_musica)
                if btn_salir_menu.collidepoint(pos_mouse):
                    estado = "MENU"

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
sys.exit()

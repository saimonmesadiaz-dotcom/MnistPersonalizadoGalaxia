import os

import numpy as np
import streamlit as st
import tensorflow as tf
from PIL import Image
from streamlit_drawable_canvas import st_canvas
from tensorflow import keras

st.set_page_config(
    page_title="Misión Matemática Espacial",
    page_icon="🚀",
    layout="wide",
)


def html(texto):
    """Markdown trata las líneas con sangría como código: se compacta el HTML."""
    limpio = " ".join(l.strip() for l in texto.splitlines() if l.strip())
    st.markdown(limpio, unsafe_allow_html=True)


# ============================================================
# ESTILOS: galaxia, estrellas titilantes, planeta y marcianitos
# ============================================================
html(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600;700&family=Nunito:wght@400;600;700&display=swap');

html, body, .stApp, .stApp p, .stApp label, .stApp li, .stApp span {
    font-family:'Nunito',sans-serif;
}

.stApp {
    color:#f4f1ff;
    background:
        radial-gradient(ellipse at 12% 8%,#4b1d8f 0,transparent 45%),
        radial-gradient(ellipse at 88% 82%,#7a1f8f 0,transparent 42%),
        linear-gradient(160deg,#080219,#150a47 55%,#2a0f63);
}

.stApp::before, .stApp::after {
    content:"";
    position:fixed;
    inset:0;
    z-index:0;
    pointer-events:none;
    background-repeat:repeat;
}

.stApp::before {
    background-image:
        radial-gradient(2px 2px at 20px 30px,#fff,transparent),
        radial-gradient(2px 2px at 90px 120px,#ffd93d,transparent),
        radial-gradient(1.5px 1.5px at 160px 60px,#fff,transparent),
        radial-gradient(2px 2px at 220px 180px,#4df0ff,transparent),
        radial-gradient(1.5px 1.5px at 60px 210px,#fff,transparent),
        radial-gradient(2.5px 2.5px at 140px 150px,#ff5fd2,transparent);
    background-size:260px 240px;
    animation:titilar 4s ease-in-out infinite alternate;
}

.stApp::after {
    background-image:
        radial-gradient(1.5px 1.5px at 40px 70px,#fff,transparent),
        radial-gradient(2px 2px at 190px 40px,#8dff6b,transparent),
        radial-gradient(1.5px 1.5px at 300px 250px,#fff,transparent),
        radial-gradient(2px 2px at 120px 310px,#ffd93d,transparent);
    background-size:410px 370px;
    animation:titilar 6s ease-in-out -2s infinite alternate;
}

@keyframes titilar {from {opacity:.45;} to {opacity:1;}}
@keyframes flotar {0%,100% {transform:translateY(0);} 50% {transform:translateY(-12px);}}
@keyframes volar {0%,100% {transform:translate(0,0) rotate(-8deg);} 50% {transform:translate(8px,-8px) rotate(4deg);}}

[data-testid="stHeader"] {background:transparent;}

.block-container {
    position:relative;
    z-index:1;
    max-width:1200px;
    padding-top:4rem;
}

.deco {
    position:fixed;
    z-index:0;
    pointer-events:none;
    opacity:.85;
    animation:flotar 6s ease-in-out infinite;
}
.deco.a {top:14%; left:3%; font-size:3.4rem;}
.deco.b {top:62%; right:3%; font-size:3rem; animation-delay:-2s;}
.deco.c {bottom:6%; left:6%; font-size:2.4rem; animation-delay:-4s;}
.deco.d {top:8%; right:7%; font-size:2.2rem; animation-delay:-1s;}

/* PORTADA */
.hero {
    text-align:center;
    padding:1.6rem 1rem 1.3rem;
    border-radius:32px;
    background:linear-gradient(135deg,rgba(77,240,255,.15),rgba(255,95,210,.17));
    border:2px solid rgba(255,255,255,.2);
    box-shadow:0 0 44px rgba(122,60,255,.4);
}

.hero .hero-t {
    font-family:'Fredoka',sans-serif;
    font-size:clamp(2rem,5vw,3.5rem);
    font-weight:700;
    line-height:1.1;
    margin:.2rem 0 .4rem;
    padding:0;
    color:#ffd93d;
    text-shadow:0 4px 0 #a3194f,0 0 30px rgba(255,217,61,.5);
}

.hero p {
    font-size:1.2rem;
    margin:0;
    color:#e7e0ff;
}

.cohete {display:inline-block; animation:volar 3s ease-in-out infinite;}

/* TARJETAS (st.container con borde) */
[data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] {
    background:rgba(20,10,60,.66);
    border:2px solid rgba(77,240,255,.38) !important;
    border-radius:26px !important;
    box-shadow:0 0 26px rgba(77,240,255,.2);
    backdrop-filter:blur(6px);
}

.titulo-tarjeta {
    font-family:'Fredoka',sans-serif;
    font-size:1.5rem;
    font-weight:600;
    color:#4df0ff;
    margin:0 0 .6rem;
}

.titulo-seccion {
    font-family:'Fredoka',sans-serif;
    font-size:1.8rem;
    font-weight:600;
    color:#ffd93d;
    margin:1.8rem 0 .7rem;
}

/* PANTALLA DE LA NAVE (lienzo) */
iframe[title*="canvas"] {
    display:block;
    width:400px !important;
    max-width:100%;
    margin:0 auto;
    border-radius:18px;
    box-shadow:0 0 0 4px #4df0ff,0 0 0 9px rgba(77,240,255,.22),0 0 40px rgba(77,240,255,.55);
}

/* BOTONES */
.stButton > button {
    font-family:'Fredoka',sans-serif;
    font-weight:600;
    font-size:1.2rem;
    border:0;
    border-radius:999px;
    padding:.75rem 1.2rem;
    transition:transform .2s ease;
}
.stButton > button p {color:inherit; font-family:'Fredoka',sans-serif; font-size:1.2rem;}
.stButton > button:hover {transform:translateY(-3px) scale(1.03);}
.stButton > button:active {transform:translateY(2px);}

.stButton > button[kind="primary"],
[data-testid="stBaseButton-primary"],
[data-testid="baseButton-primary"] {
    background:linear-gradient(135deg,#ff9f43,#ff3d81) !important;
    color:#fff !important;
    box-shadow:0 6px 0 #a3194f,0 0 26px rgba(255,61,129,.6);
}

.stButton > button[kind="secondary"],
[data-testid="stBaseButton-secondary"],
[data-testid="baseButton-secondary"] {
    background:linear-gradient(135deg,#4df0ff,#6a7bff) !important;
    color:#07123a !important;
    box-shadow:0 6px 0 #2a3fb0;
}

/* PASOS PARA JUGAR */
.paso {
    display:flex;
    align-items:center;
    gap:.8rem;
    margin:.55rem 0;
    font-size:1.1rem;
}
.paso b {
    flex-shrink:0;
    width:2.2rem;
    height:2.2rem;
    border-radius:50%;
    display:flex;
    align-items:center;
    justify-content:center;
    font-family:'Fredoka',sans-serif;
    background:#ffd93d;
    color:#2a0f63;
}

/* AVISOS */
.aviso {
    padding:1rem 1.3rem;
    border-radius:20px;
    font-size:1.1rem;
    background:rgba(255,217,61,.15);
    border:2px dashed #ffd93d;
    color:#fff3b0;
}

/* RESULTADO: el planeta con el número */
.resultado {
    display:flex;
    align-items:center;
    gap:2rem;
    flex-wrap:wrap;
    padding:1.5rem 2rem;
    border-radius:32px;
    background:linear-gradient(135deg,rgba(141,255,107,.18),rgba(77,240,255,.16));
    border:2px solid rgba(141,255,107,.6);
    box-shadow:0 0 40px rgba(141,255,107,.3);
}

.planeta {
    position:relative;
    flex-shrink:0;
    width:170px;
    height:170px;
    border-radius:50%;
    display:flex;
    align-items:center;
    justify-content:center;
    font-family:'Fredoka',sans-serif;
    font-size:6.5rem;
    font-weight:700;
    color:#fff;
    text-shadow:0 4px 0 rgba(120,20,60,.6);
    background:radial-gradient(circle at 30% 28%,#ffd93d,#ff7a3d 55%,#a3194f);
    box-shadow:0 0 46px rgba(255,150,60,.75),inset -16px -16px 30px rgba(0,0,0,.35);
    animation:flotar 4s ease-in-out infinite;
}

.planeta::after {
    content:"";
    position:absolute;
    z-index:-1;
    width:250px;
    height:48px;
    border:6px solid rgba(255,217,61,.7);
    border-radius:50%;
    transform:rotate(-18deg);
}

.resultado .res-t {
    font-family:'Fredoka',sans-serif;
    font-size:clamp(1.8rem,4vw,2.7rem);
    margin:0 0 .3rem;
    padding:0;
    color:#fff;
}
.resultado p {font-size:1.3rem; margin:.2rem 0; color:#e7ffe0;}
.estrellas {font-size:2rem; letter-spacing:.2rem;}

/* ESTADÍSTICAS DE LOS MARCIANITOS */
.stats {
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(210px,1fr));
    gap:1rem;
    margin:1.3rem 0 .5rem;
}

.stat {
    text-align:center;
    padding:1.2rem 1rem;
    border-radius:26px;
    background:rgba(20,10,60,.72);
    border:2px solid;
}
.stat .ico {font-size:3rem; line-height:1.1;}
.stat .val {font-family:'Fredoka',sans-serif; font-size:2.6rem; font-weight:700; line-height:1.1;}
.stat .lab {font-size:1.05rem; opacity:.9;}
.s1 {border-color:#ffd93d; box-shadow:0 0 24px rgba(255,217,61,.35);}
.s1 .val {color:#ffd93d;}
.s2 {border-color:#8dff6b; box-shadow:0 0 24px rgba(141,255,107,.35);}
.s2 .val {color:#8dff6b;}
.s3 {border-color:#ff5fd2; box-shadow:0 0 24px rgba(255,95,210,.35);}
.s3 .val {color:#ff5fd2;}

.energia {
    height:16px;
    margin-top:.6rem;
    border-radius:99px;
    overflow:hidden;
    background:rgba(255,255,255,.16);
}
.energia i {
    display:block;
    height:100%;
    border-radius:99px;
    background:linear-gradient(90deg,#8dff6b,#4df0ff);
}

/* BARRAS DE PROBABILIDAD */
.fila {display:flex; align-items:center; gap:.8rem; margin:.5rem 0;}
.fila .nom {
    width:4.2rem;
    flex-shrink:0;
    font-family:'Fredoka',sans-serif;
    font-size:1.3rem;
    text-align:right;
}
.pista {
    flex:1;
    height:22px;
    border-radius:99px;
    overflow:hidden;
    background:rgba(255,255,255,.12);
}
.pista i {
    display:block;
    height:100%;
    border-radius:99px;
    background:linear-gradient(90deg,#6a7bff,#4df0ff);
}
.pista i.gana {
    background:linear-gradient(90deg,#ff9f43,#ffd93d);
    box-shadow:0 0 16px rgba(255,217,61,.8);
}
.fila .pct {width:4.6rem; flex-shrink:0; font-weight:700;}

/* IMÁGENES, EXPANDER, BARRA LATERAL */
[data-testid="stImage"] img {
    border-radius:18px;
    border:3px solid #4df0ff;
    box-shadow:0 0 22px rgba(77,240,255,.45);
}

[data-testid="stExpander"] {
    border:2px solid rgba(255,95,210,.5);
    border-radius:20px;
    background:rgba(20,10,60,.6);
}
[data-testid="stExpander"] summary p {font-size:1.1rem; color:#ff9be8;}

[data-testid="stSidebar"] {
    background:linear-gradient(180deg,#120640,#2a0f63) !important;
    border-right:2px solid rgba(77,240,255,.3);
}
[data-testid="stSidebar"] * {color:#f4f1ff;}

[data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"] {
    background:none;
    border:0 !important;
    box-shadow:none;
    backdrop-filter:none;
}

.side {padding:.3rem .5rem 1rem;}

.chip {
    display:flex;
    justify-content:space-between;
    align-items:center;
    gap:.8rem;
    margin:.5rem 0;
    padding:.6rem .95rem;
    border-radius:16px;
    font-size:1rem;
    background:rgba(77,240,255,.1);
    border:1px solid rgba(77,240,255,.35);
}
.chip span {font-weight:700; color:#ffd93d !important; word-break:break-all; text-align:right;}

.stSpinner, .stSpinner * {color:#ffd93d !important; font-size:1.2rem;}

@media (max-width:700px) {
    .deco {display:none;}
    .planeta {width:130px; height:130px; font-size:4.8rem;}
    .planeta::after {width:190px; height:38px;}
    .fila .nom {width:3.2rem; font-size:1.1rem;}
}

@media (prefers-reduced-motion:reduce) {
    *, *::before, *::after {animation:none !important; transition:none !important;}
}
</style>
<div class="deco a">🪐</div>
<div class="deco b">🛸</div>
<div class="deco c">🌙</div>
<div class="deco d">☄️</div>
"""
)


# ============================================================
# MODELO
# ============================================================
@st.cache_resource
def cargar_modelo():
    """Busca y carga el modelo MNIST. Devuelve (modelo, ruta, errores)."""
    errores = []

    for ruta in ["mnist_model.keras", "mnist_model.h5"]:
        if os.path.exists(ruta):
            try:
                return keras.models.load_model(ruta), ruta, errores
            except Exception as e:
                errores.append(f"{ruta}: {e}")

    return None, None, errores


model, ruta_modelo, errores_modelo = cargar_modelo()

# ============================================================
# BARRA LATERAL
# ============================================================
with st.sidebar:
    estado = "listo" if model is not None else "no encontrado"
    archivo = ruta_modelo or "sin archivo"

    html(
        f"""
<div class="side">
<div class="titulo-tarjeta">🛰️ Panel de la nave</div>
<div class="chip">🤖 Cerebro robótico<span>{estado}</span></div>
<div class="chip">📁 Archivo<span>{archivo}</span></div>
<div class="chip">TensorFlow<span>{tf.__version__}</span></div>
<div class="chip">Keras<span>{keras.__version__}</span></div>
<div class="titulo-tarjeta" style="margin-top:1.8rem">🎒 Cómo jugar</div>
<div class="paso"><b>1</b><span>Dibuja un número del 0 al 9.</span></div>
<div class="paso"><b>2</b><span>Toca el botón de lanzar.</span></div>
<div class="paso"><b>3</b><span>Descubre qué número ve el alienígena.</span></div>
</div>
"""
    )

if model is None:
    html(
        """
<div class="aviso">No encontré el cerebro del robot. Entrena el modelo en Google
Colab, descarga <b>mnist_model.keras</b>, súbelo a la raíz del repositorio y
reinicia la aplicación.</div>
"""
    )
    for e in errores_modelo:
        st.error(f"Error al cargar {e}")
    st.stop()

# ============================================================
# PORTADA
# ============================================================
html(
    """
<div class="hero">
<div class="hero-t"><span class="cohete">🚀</span> Misión Matemática Espacial</div>
<p>Dibuja un número y el alienígena lo adivinará.</p>
</div>
"""
)

if "lienzo" not in st.session_state:
    st.session_state.lienzo = 0

# ============================================================
# LIENZO Y CONTROLES
# ============================================================
st.write("")
col_lienzo, col_control = st.columns([3, 2], gap="large")

with col_lienzo:
    with st.container(border=True):
        html('<div class="titulo-tarjeta">🖥️ Pantalla de la nave</div>')
        canvas_result = st_canvas(
            fill_color="black",
            stroke_width=20,
            stroke_color="white",
            background_color="black",
            width=400,
            height=400,
            drawing_mode="freedraw",
            display_toolbar=False,
            key=f"canvas_{st.session_state.lienzo}",
        )

with col_control:
    with st.container(border=True):
        html('<div class="titulo-tarjeta">🎮 Controles</div>')
        html(
            """
<div style="font-size:1.1rem;margin-bottom:1rem">Dibuja el número <b>grande y
centrado</b> con tu dedo o con el mouse. Si te equivocas, toca <b>Limpiar el espacio</b>
y empieza de nuevo.</div>
"""
        )
        predecir = st.button("🚀 ¡Lanzar!", type="primary", use_container_width=True)
        st.write("")
        limpiar = st.button("🧹 Limpiar el espacio", use_container_width=True)

        if limpiar:
            st.session_state.lienzo += 1
            st.rerun()

# ============================================================
# PREDICCIÓN
# ============================================================
EMOJIS = ["🌑", "🌙", "⭐", "🌟", "🪐", "☄️", "🚀", "🛸", "👽", "🌍"]
NOMBRES = [
    "cero", "uno", "dos", "tres", "cuatro",
    "cinco", "seis", "siete", "ocho", "nueve",
]

if predecir:
    if canvas_result.image_data is None:
        html('<div class="aviso">⚠️ Dibuja un número en la pantalla de la nave.</div>')
    else:
        imagen = Image.fromarray(canvas_result.image_data.astype("uint8")).convert("L")

        # Sin trazos blancos no hay nada que adivinar
        if np.max(np.array(imagen)) < 30:
            html('<div class="aviso">⚠️ La pantalla está vacía. ¡Dibuja un número primero!</div>')
        else:
            with st.spinner("👽 El alienígena está pensando..."):
                pequena = imagen.resize((28, 28), Image.Resampling.LANCZOS)
                arreglo = (np.array(pequena) / 255.0).reshape(1, 28, 28, 1)

                prediccion = model.predict(arreglo, verbose=0)
                digito = int(np.argmax(prediccion))
                confianza = float(np.max(prediccion) * 100)
                segunda = int(np.argsort(prediccion[0])[-2])

            if confianza >= 90:
                titulo, mensaje = "¡Misión cumplida!", "Estoy súper seguro 🤩"
            elif confianza >= 60:
                titulo, mensaje = "¡Casi lo tengo!", "Creo que es este número 🧐"
            else:
                titulo, mensaje = "¡Uy, qué difícil!", "Prueba dibujarlo más grande y centrado 🖍️"

            n = max(1, round(confianza / 20))
            estrellas = "⭐" * n + "☆" * (5 - n)

            html(
                f"""
<div class="titulo-seccion">🛸 Mensaje del alienígena</div>
<div class="resultado">
<div class="planeta">{digito}</div>
<div>
<div class="res-t">{titulo} Es el número {NOMBRES[digito]}</div>
<p>👽 {mensaje}</p>
<div class="estrellas">{estrellas}</div>
</div>
</div>
<div class="stats">
<div class="stat s1"><div class="ico">🪐</div><div class="val">{digito}</div>
<div class="lab">Número descubierto</div></div>
<div class="stat s2"><div class="ico">🔋</div><div class="val">{confianza:.0f}%</div>
<div class="lab">Energía del alienígena</div>
<div class="energia"><i style="width:{confianza:.0f}%"></i></div></div>
<div class="stat s3"><div class="ico">🛸</div><div class="val">{segunda}</div>
<div class="lab">Plan B: la otra idea</div></div>
</div>
"""
            )

            if confianza >= 90:
                st.balloons()

            # Imágenes
            html('<div class="titulo-seccion">🔭 Lo que vio la nave</div>')
            c1, c2 = st.columns(2)
            with c1:
                st.write("**Tu dibujo**")
                st.image(canvas_result.image_data, width=220)
            with c2:
                st.write("**Lo que ve el alienígena (28x28)**")
                st.image(pequena.resize((220, 220), Image.Resampling.NEAREST), width=220)

            # Probabilidades
            filas = ""
            for i, p in enumerate(prediccion[0] * 100):
                gana = " gana" if i == digito else ""
                marca = " 👽" if i == digito else ""
                filas += (
                    f'<div class="fila"><div class="nom">{EMOJIS[i]} {i}</div>'
                    f'<div class="pista"><i class="{gana.strip()}" '
                    f'style="width:{max(p, 1.5):.1f}%"></i></div>'
                    f'<div class="pct">{p:.1f}%{marca}</div></div>'
                )

            html('<div class="titulo-seccion">📊 ¿Qué tan seguro está cada marciano?</div>')
            with st.container(border=True):
                html(filas)

            with st.expander("🔬 Informe del científico alienígena"):
                for i, p in enumerate(prediccion[0]):
                    marca = "🎯" if i == digito else ""
                    st.write(f"{marca} **Número {i}**: {p * 100:.2f}%")

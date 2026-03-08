import streamlit as st
import os
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI

# --- 1. НАСТРОЙКА МОДЕЛИ И КЛЮЧА ---
MODEL_NAME = "gemini-2.5-flash" 
MY_API_KEY = st.secrets["GOOGLE_API_KEY"]
os.environ["GOOGLE_API_KEY"] = MY_API_KEY

# --- 2. ИНТЕРФЕЙС STREAMLIT ---
st.set_page_config(
    page_title="Адаптивный гид KazNU", 
    layout="wide", 
    page_icon="🌍",
    initial_sidebar_state="expanded"
)

# Розовый стиль для кнопок и заголовков
st.markdown("""
    <style>
    .stButton>button {
        background-color: #FF69B4;
        color: white;
        border-radius: 20px;
    }
    h1 { color: #C71585; }
    h2 { color: #DB7093; }
    </style>
    """, unsafe_allow_html=True)

# --- ЛЕВАЯ ПАНЕЛЬ (SIDEBAR) ---
with st.sidebar:
    st.image("https://raw.githubusercontent.com/snezhanw/snezhana_MP_srs2/main/1221.JPG", caption="Vibe Check!")
    st.title("💖 Настройки МАС")
    st.success(f"🤖 Модель: {MODEL_NAME}")
    st.link_button("🔥 Вступить в СББП (Instagram)", "https://www.instagram.com/sbbp_kaznu/")
    st.write("---")
    st.write("**Разработано круто и хайпово**")
    st.write("Студентка: Снежана ✨")

# --- ЦЕНТРАЛЬНАЯ ЧАСТЬ ---
st.title("🌍 Адаптивный гид для иностранных абитуриентов")

# Пытаемся загрузить фото кампуса
st.image("https://raw.githubusercontent.com/snezhanw/snezhana_MP_srs2/main/kaznu.png", caption="Кампус КазНУ им. Аль-Фараби")

st.markdown("#### Добро пожаловать в КазНУ! Наша команда агентов составит для тебя лучший маршрут.")

# --- ЗОНА 1: КОНФИГУРАЦИЯ ---
with st.expander("✨ Настрой характер своих гидов"):
    col_a, col_b = st.columns(2)
    with col_a:
        role_analyst = st.text_input("Роль Аналитика:", value="Культурный эксперт КазНУ")
        backstory_analyst = st.text_area("История Аналитика:", value="Ты профи. Помогаешь иностранцам влюбиться в КазНУ.")
    with col_b:
        role_guide = st.text_input("Роль Гида:", value="Студенческий гид СББП")
        backstory_guide = st.text_area("История Гида:", value="Ты свой парень. Знаешь всё про Спаун и лучшие донеры.")

# --- ЗОНА 2: ВВОД ДАННЫХ ---
st.header("📝 Ввод данных")
col1, col2 = st.columns(2)
with col1:
    origin_country = st.text_input("Из какой страны студенты?", value="Южная Корея")
with col2:
    campus_objects = st.text_area("Объекты кампуса:", value="1. ЦОС Керемет\n2. Библиотека Аль-Фараби\n3. Спаун / Арай донерка\n4. Общежитие №8")

# --- 4. ЛОГИКА АГЕНТОВ ---
def run_tour_process(country, objects, r_analyst, b_analyst, r_guide, b_guide):
    llm = ChatGoogleGenerativeAI(model=MODEL_NAME, google_api_key=MY_API_KEY)
    
    analyst = Agent(role=r_analyst, goal=f'Адаптация для студентов из {country}', backstory=b_analyst, llm=llm)
    guide = Agent(role=r_guide, goal=f'Составить лучший маршрут по {objects}', backstory=b_guide, llm=llm)

    t1 = Task(description=f"3 совета для студентов из {country} при посещении КазНУ.", expected_output="Культурные советы.", agent=analyst)
    t2 = Task(description=f"Напиши крутой гид по местам: {objects}. В конце позови в СББП!", expected_output="Текст гида на русском языке.", agent=guide)

    crew = Crew(agents=[analyst, guide], tasks=[t1, t2], process=Process.sequential)
    return crew.kickoff()

# --- ЗОНА 3: ЗАПУСК ---
if st.button("🌟 Сгенерировать гид и вступить в движ", width='stretch'):
    with st.status("🤖 Агенты обсуждают маршрут...", expanded=True) as status:
        try:
            result = run_tour_process(origin_country, campus_objects, role_analyst, backstory_analyst, role_guide, backstory_guide)
            status.update(label="✅ Готово!", state="complete", expanded=False)
            st.markdown("### ✨ Твой персональный гид")
            st.markdown(result.raw)
            st.balloons()
        except Exception as e:
            st.error(f"Ошибка: {e}")

import streamlit as st
import os
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI

MODEL_NAME = "gemini-2.5-flash" 

if "GOOGLE_API_KEY" in st.secrets:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
    MY_API_KEY = st.secrets["GOOGLE_API_KEY"]
else:
    st.error("Критическая ошибка: GOOGLE_API_KEY не найден в Secrets приложения!")
    st.stop()

# --- 2. ИНТЕРФЕЙС И СТИЛИЗАЦИЯ ---
st.set_page_config(
    page_title="Адаптивный гид KazNU", 
    layout="wide", 
    page_icon="🌍"
)

# Розовый хайповый стиль
st.markdown("""
    <style>
    .stButton>button {
        background-color: #FF69B4;
        color: white;
        border-radius: 20px;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #FF1493;
        color: white;
    }
    h1 { color: #C71585; }
    h2 { color: #DB7093; }
    .stStatus { border-color: #FF69B4; }
    </style>
    """, unsafe_allow_html=True)

# --- ЛЕВАЯ ПАНЕЛЬ (SIDEBAR) ---
with st.sidebar:
    # Используем прямую ссылку на фото из твоего GitHub
    st.image("https://raw.githubusercontent.com/snezhanw/snezhana_MP_srs2/main/1221.JPG", 
             caption="Vibe Check! ✨")
    
    st.title("💖 wwwwwwwwwww")
    st.success(f"🤖 Модель: {MODEL_NAME}")
    
    st.link_button("🔥 Вступить в СББП (Instagram)", "https://www.instagram.com/sbbp_kaznu/")
    
    st.write("---")
    st.write("**Разработано круто и хайпово**")
    st.write("Студентка: Снежана")
    st.write("Университет: КазНУ (FIT)")

# --- ЦЕНТРАЛЬНАЯ ЧАСТЬ ---
st.title("🌍 Адаптивный гид для иностранных абитуриентов")

st.image("https://raw.githubusercontent.com/snezhanw/snezhana_MP_srs2/main/kaznu.png", 
         caption="Кампус КазНУ им. Аль-Фараби")

st.markdown("#### Добро пожаловать! Твои ИИ-гиды помогут тебе освоиться в кампусе.")

# --- ЗОНА 1: КОНФИГУРАЦИЯ АГЕНТОВ ---
with st.expander("✨ Настрой характер своих гидов"):
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Агент-Аналитик")
        role_analyst = st.text_input("Роль:", value="Культурный эксперт КазНУ")
        backstory_analyst = st.text_area("История:", 
                                         value="Ты профи в межкультурной коммуникации. Помогаешь иностранцам понять традиции Казахстана и КазНУ.")
    with col_b:
        st.subheader("Агент-Гид")
        role_guide = st.text_input("Роль :", value="Студенческий гид СББП")
        backstory_guide = st.text_area("История :", 
                                       value="Ты свой парень в кампусе. Знаешь всё про Спаун, Арай донерку и как быстро найти друзей.")

# --- ЗОНА 2: ВВОД ДАННЫХ ---
st.header("📝 Ввод данных")
col1, col2 = st.columns(2)
with col1:
    origin_country = st.text_input("Из какой страны студенты?", value="Южная Корея")
with col2:
    campus_objects = st.text_area(
        "Объекты кампуса:", 
        value="1. ЦОС Керемет\n2. Библиотека Аль-Фараби\n3. Спаун / Арай донерка\n4. Общежитие №8",
        height=100
    )

# --- 3. ЛОГИКА МУЛЬТИАГЕНТНОЙ СИСТЕМЫ ---
def run_tour_process(country, objects, r_analyst, b_analyst, r_guide, b_guide):
    llm = ChatGoogleGenerativeAI(model=MODEL_NAME, google_api_key=MY_API_KEY)

    # Создание агентов
    analyst = Agent(
        role=r_analyst, 
        goal=f'Подготовить культурную адаптацию для студентов из {country}', 
        backstory=b_analyst, 
        llm=llm
    )
    
    guide = Agent(
        role=r_guide, 
        goal=f'Составить лучший маршрут по локациям: {objects}', 
        backstory=b_guide, 
        llm=llm
    )

    # Задачи
    t1 = Task(
        description=f"Дай 3 важных совета для студентов из {country} о том, как вести себя в КазНУ.", 
        expected_output="Список из 3 культурных советов.", 
        agent=analyst
    )
    
    t2 = Task(
        description=f"Напиши крутой и понятный гид по местам: {objects}. В конце добавь фразу: 'Вступай в СББП! Это лучший способ найти друзей!'", 
        expected_output="Текст гида на русском языке.", 
        agent=guide
    )

    # Сборка команды
    crew = Crew(
        agents=[analyst, guide], 
        tasks=[t1, t2], 
        process=Process.sequential
    )
    
    return crew.kickoff()

# --- ЗОНА 3: ЗАПУСК ---
st.divider()
if st.button("🚀 Сгенерировать гид и вступить в движ", use_container_width=True):
    with st.status("🤖 Агенты CrewAI анализируют запрос...", expanded=True) as status:
        try:
            result = run_tour_process(
                origin_country, 
                campus_objects, 
                role_analyst, 
                backstory_analyst, 
                role_guide, 
                backstory_guide
            )
            status.update(label="✅ Гид успешно составлен!", state="complete", expanded=False)
            
            st.markdown("### ✨ Результат работы агентов:")
            st.markdown(result) 
            st.balloons()

            st.download_button("📥 Скачать гид (.md)", str(result), file_name="kaznu_guide.md")
        except Exception as e:
            st.error(f"Произошла ошибка: {e}")

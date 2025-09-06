import streamlit as st
from datetime import datetime
import sys

# --- Guard: ensure the script is run with `streamlit run` ---
try:
    from streamlit.runtime.scriptrunner import get_script_run_ctx
    in_streamlit = get_script_run_ctx() is not None
except Exception:
    in_streamlit = False

if not in_streamlit:
    print("This app must be started with: streamlit run learner_portal_app.py")
    sys.exit(0)

# --- initialize session state safely ---
def init_state():
    if "users" not in st.session_state:
        st.session_state.users = {}
    if "materials" not in st.session_state:
        st.session_state.materials = [
            {"title": "Presentation I", "https://github.com/CDAMChukaUniversity/2025-AMMnet_Malaria_Modeling_Workshop/blob/main/Presentation-I.pdf": "Presentation-I.pdf"},
            {"title": "Presentation II", "link": "https://github.com/AMMNetMachineLearningGroup/APP2025/blob/main/EXplainable-AI.pdf"},
            {"title": "Presentation III", "link": "https://github.com/AMMNetMachineLearningGroup/APP2025/blob/main/AI_in_Modeling_Balancing_Innovation_with_Ethics.pdf"},
        ]


def main():
    init_state()

    st.title("📚 CDAM-Chuka University")
    st.write("Welcome! Register and access your training materials.")

    menu = ["Register", "Login", "Training Materials", "Certificate"]
    choice = st.sidebar.selectbox("Menu", menu)

    # --- REGISTRATION ---
    if choice == "Register":
        st.subheader("Create a New Account")
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Register"):
            if not username:
                st.warning("Please enter a username.")
            elif username in st.session_state.users:
                st.warning("⚠️ Username already exists.")
            else:
                st.session_state.users[username] = {
                    "email": email,
                    "password": password,
                    "completed": False,
                }
                st.success("✅ Registration successful! Please login.")

    # --- LOGIN ---
    elif choice == "Login":
        st.subheader("Login to Your Account")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login"):
            user = st.session_state.users.get(username)
            if user and user["password"] == password:
                st.success(f"Welcome back {username}!")
            else:
                st.error("❌ Invalid credentials.")

    # --- TRAINING MATERIALS ---
    elif choice == "Training Materials":
        st.subheader("Your Training Materials")
        username = st.text_input("Enter your username for materials", key="materials_username")

        user = st.session_state.users.get(username)
        if user:
            for material in st.session_state.materials:
                st.markdown(f"📖 [{material['title']}]({material['link']})")

            if st.button("Mark Course as Completed"):
                user["completed"] = True
                st.success("🎉 Congratulations! You completed the training.")
        else:
            st.info("User not found. Please register/login.")

    # --- CERTIFICATE ---
    elif choice == "Certificate":
        st.subheader("Download Your Certificate")
        username = st.text_input("Enter your username to download certificate", key="cert_username")

        user = st.session_state.users.get(username)
        if user and user.get("completed"):
            cert_text = f"""Certificate of Completion\n\nThis certifies that {username} has successfully completed the training.\nDate: {datetime.today().strftime('%Y-%m-%d')}\n"""
            st.download_button("⬇️ Download Certificate", cert_text, file_name=f"{username}_certificate.txt")
        elif user:
            st.info("🚀 Complete all training materials to unlock your certificate.")
        else:
            st.info("User not found. Please register/login.")


if __name__ == "__main__":
    main()

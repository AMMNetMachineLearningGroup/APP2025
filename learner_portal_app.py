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
    # If you run this with `python learner_portal_app.py` or inside a plain Jupyter cell
    # Streamlit will emit repeated "missing ScriptRunContext" warnings. Exit early
    # with a friendly message so the warnings don't flood the terminal.
    print("This app must be started with: streamlit run learner_portal_app.py")
    sys.exit(0)

# --- initialize session state safely ---
def init_state():
    if "users" not in st.session_state:
        st.session_state.users = {}
    if "materials" not in st.session_state:
        st.session_state.materials = [
            {"title": "Intro to Data Science", "link": "materials/intro.pdf"},
            {"title": "Statistics Basics", "link": "materials/stats.pdf"},
            {"title": "Machine Learning 101", "link": "materials/ml101.pdf"},
        ]


def main():
    init_state()

    st.title("📚 Training Platform")
    st.write("Welcome! Register, pay, and access your training materials.")

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
                    "paid": False,
                    "completed": False,
                }
                st.success("✅ Registration successful! Please login.")

    # --- LOGIN & PAYMENT ---
    elif choice == "Login":
        st.subheader("Login to Your Account")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login"):
            user = st.session_state.users.get(username)
            if user and user["password"] == password:
                st.success(f"Welcome back {username}!")

                if not user["paid"]:
                    st.info("💳 Please make payment to unlock materials.")
                    if st.button("Simulate Payment (KES 2000)"):
                        user["paid"] = True
                        st.success("✅ Payment successful! You can now access training materials.")
            else:
                st.error("❌ Invalid credentials.")

    # --- TRAINING MATERIALS ---
    elif choice == "Training Materials":
        st.subheader("Your Training Materials")
        username = st.text_input("Enter your username for materials", key="materials_username")

        user = st.session_state.users.get(username)
        if user:
            if user["paid"]:
                for material in st.session_state.materials:
                    st.markdown(f"📖 [{material['title']}]({material['link']})")

                if st.button("Mark Course as Completed"):
                    user["completed"] = True
                    st.success("🎉 Congratulations! You completed the training.")
            else:
                st.warning("⚠️ Please complete payment first.")
        else:
            st.info("User not found. Please register/login.")

    # --- CERTIFICATE ---
    elif choice == "Certificate":
        st.subheader("Download Your Certificate")
        username = st.text_input("Enter your username to download certificate", key="cert_username")

        user = st.session_state.users.get(username)
        if user and user.get("completed"):
            cert_text = f"""Certificate of Completion

This certifies that {username} has successfully completed the training.
Date: {datetime.today().strftime('%Y-%m-%d')}
"""
            st.download_button("⬇️ Download Certificate", cert_text, file_name=f"{username}_certificate.txt")
        elif user:
            st.info("🚀 Complete all training materials to unlock your certificate.")
        else:
            st.info("User not found. Please register/login.")


if __name__ == "__main__":
    main()

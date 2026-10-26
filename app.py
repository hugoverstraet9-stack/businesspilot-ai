
import streamlit as st
import sqlite3
from datetime import date

st.set_page_config(page_title="BusinessPilot AI", page_icon="🚀", layout="wide")

st.title("🚀 BusinessPilot AI")
st.caption("Ton assistant de gestion d'entreprise")

db = sqlite3.connect("businesspilot.db", check_same_thread=False)
db.execute("""
CREATE TABLE IF NOT EXISTS prospects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    entreprise TEXT DEFAULT '',
    statut TEXT DEFAULT 'Nouveau',
    notes TEXT DEFAULT ''
)
""")
db.commit()

page = st.sidebar.radio(
    "Menu",
    ["Tableau de bord", "Prospects", "Ajouter un prospect", "Assistant business"]
)

if page == "Tableau de bord":
    st.header("📊 Tableau de bord")
    total = db.execute("SELECT COUNT(*) FROM prospects").fetchone()[0]
    a, b = st.columns(2)
    a.metric("Prospects enregistrés", total)
    b.metric("Date du jour", date.today().strftime("%d/%m/%Y"))
    st.info("Ajoute tes premiers prospects pour commencer.")

elif page == "Prospects":
    st.header("👥 Mes prospects")
    rows = db.execute(
        "SELECT id, nom, entreprise, statut, notes FROM prospects ORDER BY id DESC"
    ).fetchall()
    if rows:
        for ident, nom, entreprise, statut, notes in rows:
            with st.expander(f"{nom} — {entreprise or 'Sans entreprise'}"):
                st.write("Statut :", statut)
                st.write("Notes :", notes or "Aucune note")
                if st.button("Supprimer", key=f"del_{ident}"):
                    db.execute("DELETE FROM prospects WHERE id = ?", (ident,))
                    db.commit()
                    st.rerun()
    else:
        st.write("Aucun prospect pour le moment.")

elif page == "Ajouter un prospect":
    st.header("➕ Ajouter un prospect")
    with st.form("prospect_form"):
        nom = st.text_input("Nom du contact *")
        entreprise = st.text_input("Entreprise")
        statut = st.selectbox(
            "Statut",
            ["Nouveau", "À contacter", "Contacté", "Client", "Perdu"]
        )
        notes = st.text_area("Notes")
        valide = st.form_submit_button("Enregistrer")
    if valide:
        if nom.strip():
            db.execute(
                "INSERT INTO prospects (nom, entreprise, statut, notes) VALUES (?, ?, ?, ?)",
                (nom.strip(), entreprise.strip(), statut, notes.strip())
            )
            db.commit()
            st.success("Prospect enregistré !")
        else:
            st.error("Entre au moins le nom du contact.")

elif page == "Assistant business":
    st.header("🧠 Assistant business")
    st.write("Prépare tes idées avant de contacter un prospect.")
    activite = st.text_input("Activité de l'entreprise")
    probleme = st.text_area("Quel problème veux-tu résoudre ?")
    if st.button("Préparer une analyse"):
        if activite.strip() and probleme.strip():
            st.subheader("Pistes à explorer")
            st.write("**Entreprise :**", activite)
            st.write("**Problème identifié :**", probleme)
            st.write("**Questions à poser :**")
            st.write("- Comment gérez-vous ce problème actuellement ?")
            st.write("- Combien de temps cela vous prend-il ?")
            st.write("- Quel résultat serait le plus utile pour vous ?")
            st.warning("Ce sont des pistes de réflexion, pas des faits vérifiés.")
        else:
            st.error("Remplis les deux champs.")

db.close()

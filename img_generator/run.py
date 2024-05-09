import streamlit as st
import replicate


def configure_sidebar():
    with st.sidebar:
        st.title("Image Generator")
        with st.form("my_form"):
            width = st.number_input(
                "Width", min_value=256, max_value=2024, value=1920, step=8
            )

            hight = st.number_input(
                "Hight", min_value=256, max_value=2024, value=1024, step=8
            )

            image_link = st.text_input("Image Link: ")

            prompt = st.text_area("Prompt: ")

            submitted = st.form_submit_button("Click", type="primary")

        return {
            "width": width,
            "hight": hight,
            "prompt": prompt,
            "submitted": submitted,
            "image_link": image_link,
        }


def main_page(width: int, hight: int, prompt: str, submitted: bool, image_link: str):
    if submitted:
        with st.spinner("Loading..."):
            res = replicate.run(
                "zsxkib/pulid:c169c3b8f6952cf895d043d7b56830b4e9a3e9409a026004e9efbd9da42912b4",
                input={
                    "prompt": prompt,
                    "negative_prompt": "flaws in the eyes, flaws in the face, flaws, lowres, non-HDRi, low quality, worst quality,artifacts noise, text, watermark, glitch, deformed, mutated, ugly, disfigured, hands, low resolution, partially rendered objects,  deformed or partially rendered eyes, deformed, deformed eyeballs, cross-eyed,blurry",
                    "image_width": width,
                    "image_height": hight,
                    "cfg_scale": 1.2,
                    "num_steps": 10,
                    "num_samples": 1,
                    "output_format": "webp",
                    "identity_scale": 0.85,
                    "mix_identities": False,
                    "output_quality": 80,
                    "generation_mode": "fidelity",
                    "main_face_image": (
                        image_link
                        if image_link
                        else "https://replicate.delivery/pbxt/Kr6iendsvYS0F3MLmwRZ8q07XIMEJdemnQI3Cmq9nNrauJbq/zcy.webp"
                    ),
                },
            )

            image = res[0]

            with st.container():
                st.image(image)


def main():
    st.set_page_config(
        page_title="Ex-stream-ly Cool App",
        page_icon="🧊",
        layout="wide",
    )

    data = configure_sidebar()
    main_page(**data)


if __name__ == "__main__":
    main()

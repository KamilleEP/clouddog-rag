import streamlit as st
import requests
import base64

PAGE_SELECTION_KEY = "page_selection"
ENDPOINT_URL = "https://3j1u3b5524.execute-api.us-east-1.amazonaws.com"

selected_archives = []

if PAGE_SELECTION_KEY not in st.session_state:
    st.session_state[PAGE_SELECTION_KEY] = "Adicione Empresa"

create_company_page = st.sidebar.button("Adicione Empresa")
update_company_page = st.sidebar.button("Atualize Empresa")
company_page = st.sidebar.button("Empresas")
chat_page = st.sidebar.button("Chat")

if create_company_page:
    st.session_state[PAGE_SELECTION_KEY] = "Adicione Empresa"
elif company_page:
    st.session_state[PAGE_SELECTION_KEY] = "Empresas"
elif chat_page:
    st.session_state[PAGE_SELECTION_KEY] = "Chat"
elif update_company_page:
    st.session_state[PAGE_SELECTION_KEY] = "Atualize Empresa"

if st.session_state[PAGE_SELECTION_KEY] == "Adicione Empresa":
    st.title("🏢 Adicione Empresa")
    id = st.text_input("Empresa ID")
    company_name = st.text_input("Nome da Empresa")
    prompt = st.text_input("Prompt")

    st.write("Selecione uma opção:")
    option = st.radio("Escolha entre passar um documento ou uma lista de URLs", ("Documento", "Links"))

    if option == "Documento":
        document_type = st.selectbox("Tipo de Documento", ["csv", "pdf", "txt"])

        document_file = st.file_uploader("Upload", type=["csv", "pdf", "txt"])

        create_company_button = st.button("Adicionar Empresa", key="create_company")

        if create_company_button and document_file:
            base64_content = base64.b64encode(document_file.getvalue()).decode()

            api_data = {
                "company_id": id,
                "company_name": company_name,
                "prompt": prompt,
                "documentType": document_type,
                "documentContent": base64_content,
            }

            try:
                response = requests.post(ENDPOINT_URL + "/company", json=api_data)
                if response.status_code == 200:
                    st.success(f"Empresa '{company_name}' criada com sucesso!")
                else:
                    st.error("Falha ao criar a empresa. Por favor, tente novamente.")
            except Exception as e:
                st.error(f"Um erro ocorreu: {str(e)}")

    elif option == "Links":
        st.subheader("Lista de URLs")
        urls = st.text_input("Novo item")

        if "lista" not in st.session_state:
            st.session_state["lista"] = []

        if st.button('Adicionar'):
            if urls:
                st.session_state.lista.append(urls)

        if st.session_state.lista:
            lista_str = "\n".join(st.session_state.lista)
            st.text_area("Itens da Lista", value=lista_str, height=200)

        create_company_button = st.button("Adicionar Empresa", key="create_company")

        if create_company_button and st.session_state.lista:

            api_data = {
                "company_id": id,
                "company_name": company_name,
                "prompt": prompt,
                "urls": st.session_state.lista
            }

            try:
                response = requests.post(ENDPOINT_URL + "/company", json=api_data)
                if response.status_code == 200:
                    st.success(f"Empresa '{company_name}' criada com sucesso!")
                else:
                    st.error("Falha ao criar a empresa. Por favor, tente novamente.")
            except Exception as e:
                st.error(f"Um erro ocorreu: {str(e)}")

elif st.session_state[PAGE_SELECTION_KEY] == "Atualize Empresa":
    st.title("🔄 Atualize Empresa")

    try:
        response = requests.get(ENDPOINT_URL + "/company")
        if response.status_code == 200:
            companies = response.json()
            company_id_options = [company["name"] for company in companies]
        else:
            st.error("Falha ao obter a lista de empresas. Por favor, tente novamente.")
            st.stop()
    except Exception as e:
        st.error(f"Um erro ocorreu: {str(e)}")
        st.stop()

    selected_company_name = st.selectbox("Selecione a Empresa", company_id_options)

    selected_company_id = next(
        (company['id'] for company in companies if company["name"] == selected_company_name),
        None,
    )


    option = st.radio("Escolha entre passar um documento ou uma lista de URLs", ("Documento", "Links"))

    if option == "Documento":
        document_type = st.selectbox("Tipo de Documento", ["csv", "txt"])
        document_file = st.file_uploader("Upload", type=["csv", "txt"])

        update_company_button = st.button("Atualizar Empresa", key="update_company")

        if update_company_button and document_file:
            base64_content = base64.b64encode(document_file.getvalue()).decode()

            api_data = {
                "id": selected_company_id,
                "documentType": document_type,
                "documentContent": base64_content,
            }

            try:
                response = requests.patch(ENDPOINT_URL + "/company", json=api_data)
                if response.status_code == 200:
                    st.success(f"Empresa '{selected_company_name}' atualizada com sucesso!")
                else:
                    st.error("Falha ao atualizar a empresa. Por favor, tente novamente.")
            except Exception as e:
                st.error(f"Um erro ocorreu: {str(e)}")

    elif option == "Links":
        st.subheader("Lista de URLs")
        urls = st.text_input("Novo item")

        if "lista" not in st.session_state:
            st.session_state["lista"] = []

        if st.button('Adicionar'):
            if urls:
                st.session_state.lista.append(urls)

        if st.session_state.lista:
            lista_str = "\n".join(st.session_state.lista)
            st.text_area("Itens da Lista", value=lista_str, height=200)

        update_company_button = st.button("Atualizar Empresa", key="update_company")

        if update_company_button and st.session_state.lista:

            api_data = {
                "company_id": selected_company_id,
                "prompt": prompt,
                "urls": st.session_state.lista
            }

            try:
                response = requests.post(ENDPOINT_URL + "/company", json=api_data)
                if response.status_code == 200:
                    st.success(f"Empresa '{selected_company_name}' atualizada com sucesso!")
                else:
                    st.error("Falha ao atualizar a empresa. Por favor, tente novamente.")
            except Exception as e:
                st.error(f"Um erro ocorreu: {str(e)}")

if st.session_state[PAGE_SELECTION_KEY] == "Empresas":
    st.title("🏢 Empresas")

    try:
        response = requests.get(ENDPOINT_URL + "/company")
        if response.status_code == 200:
            data = response.json()
        else:
            st.error("Falha ao trazer empresas. Por favor, tente novamente.")
    except Exception as e:
        st.error(f"Um erro ocorreu: {str(e)}")

    if 'data' in locals():
        for i, company in enumerate(data):
            st.text_input(label='Company Name', value=company['name'], disabled=True, key=f"checkbox_{company['name']}-{i}")

            company_id = company['id']

            # Verificar se o campo 'sync' existe e é False
            if 'sync' in company and company['sync'] == False:
                st.warning("Esta empresa ainda não foi sincronizada.")

            # try:
            #     response = requests.get(ENDPOINT_URL + f"/company/{company_id}")
            #     if response.status_code == 200:
            #         items = response.json()
            #     else:
            #         st.error("Falha ao trazer arquivos. Por favor, tente novamente.")
            # except Exception as e:
            #     st.error(f"Um erro ocorreu: {str(e)}")

            items = company['archives']

            if items is not None and items:
                for i, archive in enumerate(company['archives']):
                    checkbox_selected = st.checkbox(f"🔗 {archive['archive_name']}", key=f"checkbox_{company_id}_{archive['archive_name']}-{i}")
                    if checkbox_selected:
                        selected_archives.append(archive['archive_name'])

                delete_path = st.button("Excluir", key=f"delete_{company_id}_{i}")

                if delete_path:
                    body = {
                        "paths": selected_archives
                    }
                    
                    try:
                        response = requests.post(ENDPOINT_URL + f"/company/{company_id}/delete", json=body)
                        if response.status_code == 200:
                            st.success(f"Arquivo excluído com sucesso!")
                        else:
                            st.error("Falha ao excluir os arquivos. Por favor, tente novamente.")
                    except Exception as e:
                        st.error(f"Um erro ocorreu: {str(e)}")
elif st.session_state[PAGE_SELECTION_KEY] == "Chat":
    st.title("💬 Chatbot")

    try:
        response = requests.get(ENDPOINT_URL + "/company")
        if response.status_code == 200:
            companies = response.json()
            print('companies', companies)
            company_id_options = [company["name"] for company in companies]
        else:
            st.error("Falha ao obter a lista de empresas. Por favor, tente novamente.")
            st.stop()
    except Exception as e:
        st.error(f"Um erro ocorreu: {str(e)}")
        st.stop()

    selected_company_name = st.selectbox("Empresa", company_id_options)

    selected_company_id = next(
        (company['id'] for company in companies if company["name"] == selected_company_name),
        None,
    )

    print('selected_company_id', selected_company_id)

    models = {
        "claude-v3-sonnet": "anthropic.claude-3-sonnet-20240229-v1:0",
        "claude-v3-haiku": "anthropic.claude-3-haiku-20240307-v1:0",
    }

    model_id_options = list(models.keys())

    selected_model_id = st.selectbox("Modelo", model_id_options)
    show_citations = st.checkbox("Mostrar citações")

    chosen_company_id = selected_company_id
    chosen_model_id = models[selected_model_id]

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "Como posso ajudar você?"}
        ]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        request_data = {
            "question": prompt,
            "companyId": chosen_company_id,
            "modelId": chosen_model_id,
        }

        print('request_data', request_data)

        try:
            response = requests.post(ENDPOINT_URL + "/chat", json=request_data)
            if response.status_code == 200:
                response_data = response.json()
                response_text = response_data["response"]

                st.session_state.messages.append(
                    {"role": "assistant", "content": response_text}
                )
                st.chat_message("assistant").write(response_text)

                print(f"Response data: {response_data}")

                if show_citations:
                    if "citation" in response_data:
                        for citation_block in response_data["citation"]:
                            citation_text = citation_block["content"]["text"]
                            document_uri = citation_block["location"]["s3Location"]["uri"]
                            document_name = citation_block["metadata"]["name"]

                            st.markdown(f"**Citation from document:** {document_name}")
                            st.markdown(f"**Document URI:** {document_uri}")
                            st.markdown(f"**Content:**\n{citation_text}")
                            st.markdown("---")
            else:
                st.error("Falhou em obter uma resposta da api.")
        except Exception as e:
            st.error(f"Ocorreu um erro ao tentar enviar o pedido.")

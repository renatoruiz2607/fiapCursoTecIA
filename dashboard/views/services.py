import streamlit as st

import common
import launcher

st.title("🧰 Serviços")
st.caption(
    "Dispare cada serviço das fases anteriores por botão. "
    "Os mesmos serviços estão disponíveis no terminal pelo launcher."
)

running_servers = common.get_running_servers()

if "service_outputs" not in st.session_state:
    st.session_state.service_outputs = {}


def run_task(service, extra_args=None):
    with st.spinner(f"Executando: {service.name}..."):
        try:
            result = launcher.run_service(
                service.key,
                capture_output=True,
                extra_args=extra_args,
            )
            st.session_state.service_outputs[service.key] = {
                "success": result.returncode == 0,
                "output": (result.stdout or "") + (result.stderr or ""),
            }
        except RuntimeError as error:
            st.session_state.service_outputs[service.key] = {
                "success": False,
                "output": f"Não foi possível executar o serviço:\n{error}",
            }


def render_task(service):
    extra_args = None
    allowed = True

    if service.confirm:
        st.warning(service.confirm, icon="⚠️")
        allowed = st.checkbox("Confirmo a operação", key=f"confirm-{service.key}")
        extra_args = service.confirm_args

    if st.button("Executar", key=f"run-{service.key}", disabled=not allowed):
        run_task(service, extra_args)

    result = st.session_state.service_outputs.get(service.key)

    if result:
        if result["success"]:
            st.success("Execução concluída.")
        else:
            st.error("A execução terminou com erro ou pendência.")

        st.code(result["output"].strip() or "(sem saída)", language="text")


def render_server(service):
    process = running_servers.get(service.key)
    is_running = process is not None and process.poll() is None

    if is_running:
        st.success(f"Em execução: [{service.url}]({service.url})")

        if st.button("Parar", key=f"stop-{service.key}"):
            process.terminate()
            running_servers.pop(service.key, None)
            st.rerun()
    elif st.button("Iniciar", key=f"start-{service.key}"):
        try:
            running_servers[service.key] = launcher.run_service(service.key)
            st.rerun()
        except RuntimeError as error:
            st.error(str(error))


def render_interactive(service):
    st.info(
        "Este serviço é um menu interativo e precisa do teclado no terminal. "
        "Execute o comando abaixo na raiz do projeto:",
        icon="⌨️",
    )
    st.code(f"python launcher.py run {service.key}", language="bash")


renderers = {
    launcher.KIND_TASK: render_task,
    launcher.KIND_SERVER: render_server,
    launcher.KIND_INTERACTIVE: render_interactive,
}

phases = [phase for phase in launcher.PHASES if phase != "Dashboard"]
tabs = st.tabs([f"{phase}" for phase in phases])

for tab, phase in zip(tabs, phases):
    with tab:
        st.subheader(f"{phase} · {launcher.PHASES[phase]}")

        for service in launcher.SERVICES:
            if service.phase != phase:
                continue

            with st.container(border=True):
                st.markdown(f"**{service.name}**")
                st.caption(service.description)
                renderers[service.kind](service)

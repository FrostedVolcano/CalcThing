import streamlit as st
from posthog import Posthog
from current_divider import current_divider_tab
from voltage_divider import voltage_divider_tab
from wye_to_delta import wye_to_delta_tab
from delta_to_wye import delta_to_wye_tab
import streamlit.components.v1 as components


# Set page config first, before any other Streamlit commands
st.set_page_config(page_title="CalcThing", page_icon="logo.png", layout="wide")


st.markdown("""
<style>
    [data-testid="stDecoration"] {
        display: none;
    }
</style>
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 0rem;
        max-width: 90%;
        margin-left: auto;
        margin-right: auto;
    }
</style>
""", unsafe_allow_html=True)


posthog = Posthog('phc_WqSMXohypdxpBdGEFrJBIcTwzn0f1yKauzKY6UbxJHg', host='https://us.i.posthog.com')


st.header("CalcThing: Calculator for various things")
st.write("Visual Calculators for wye (Y) to delta (Δ) and delta (Δ) to wye (Y) circuits, voltage from voltage divider, current from parallel resistors, and many more coming!")


def main():
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Wye(Y) to Delta(Δ)", "Delta(Δ) to Wye(Y)", "Current Divider Rule", "Voltage Divider Rule"])
    
    # Render content based on active tab
    with tab1:
        wye_to_delta_tab()
    
    with tab2:
        delta_to_wye_tab()
        
    with tab3:
        current_divider_tab()
        
    with tab4:
        voltage_divider_tab()
    
if __name__ == "__main__":
    main()
    
# Keep this part at the end.
components.html("""
<head>
<script>
    !function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.crossOrigin="anonymous",p.async=!0,p.src=s.api_host.replace(".i.posthog.com","-assets.i.posthog.com")+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e},u.people.toString=function(){return u.toString(1)+".people (stub)"},o="init capture register register_once register_for_session unregister unregister_for_session getFeatureFlag getFeatureFlagPayload isFeatureEnabled reloadFeatureFlags updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures on onFeatureFlags onSessionId getSurveys getActiveMatchingSurveys renderSurvey canRenderSurvey getNextSurveyStep identify setPersonProperties group resetGroups setPersonPropertiesForFlags resetPersonPropertiesForFlags setGroupPropertiesForFlags resetGroupPropertiesForFlags reset get_distinct_id getGroups get_session_id get_session_replay_url alias set_config startSessionRecording stopSessionRecording sessionRecordingStarted captureException loadToolbar get_property getSessionProperty createPersonProfile opt_in_capturing opt_out_capturing has_opted_in_capturing has_opted_out_capturing clear_opt_in_out_capturing debug".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);
    posthog.init('phc_WqSMXohypdxpBdGEFrJBIcTwzn0f1yKauzKY6UbxJHg', {api_host: 'https://us.i.posthog.com'})
</script>
</head>
    """)

from bs4 import BeautifulSoup
import pathlib
import shutil
import streamlit as st


GA_ID = "google_analytics"
GA_SCRIPT = """
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-MV9J8KVL');</script>
<!-- End Google Tag Manager -->

<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XQQQ8NSB2Y"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('config', 'G-XQQQ8NSB2Y');
</script>
"""

GA_NOSCRIPT = """
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-MV9J8KVL"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->
"""

SEO_TAGS = """
<title>CalcThing - Circuit calculator with visualization and file format conversion</title>
<meta name="description" content="Interactive visual calculator for engineering and physics. Calculate and visualize circuits, fluid mechanics, and more in real-time. Features include Wye-Delta conversion, voltage dividers, current dividers, led current limiter circuit and fluid dynamics calculations.">

<!-- Google AdSense -->
<meta name="google-adsense-account" content="ca-pub-6414688600235144">

<!-- Additional SEO meta tags -->
<meta name="keywords" content="visual calculator, engineering calculator, physics calculator, circuit calculator, fluid mechanics, wye-delta conversion, voltage divider, current divider, led current limiting resistor real-time visualization, engineering tools">
<meta name="author" content="CalcThing">
<meta name="robots" content="index, follow">

<!-- Open Graph tags for social media -->
<meta property="og:title" content="CalcThing - Visual Calculator for Engineering & Physics">
<meta property="og:description" content="Interactive visual calculator for engineering and physics. Calculate and visualize circuits, fluid mechanics, and more in real-time.">
<meta property="og:type" content="website">
<meta property="og:site_name" content="CalcThing">

<meta name="description" content="Free online file converter supporting CSV, Excel, and PDF conversions. Convert between CSV, Excel, and PDF formats easily.">
<meta name="keywords" content="file converter, CSV to Excel, Excel to CSV, CSV to PDF, PDF to CSV, Excel to PDF, PDF to Excel, document conversion, file format converter">
<meta name="author" content="Your Name">

<!-- Open Graph meta tags for social media -->
<meta property="og:title" content="File Format Converter - CSV, Excel & PDF">
<meta property="og:description" content="Free online tool to convert between CSV, Excel, and PDF formats. Easy file conversion with multiple format support.">
<meta property="og:type" content="Calcthing">
<meta property="og:url" content="calcthing.onrender.com">
"""

PS_SCRIPT = """
<head>
<script>
    !function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.crossOrigin="anonymous",p.async=!0,p.src=s.api_host.replace(".i.posthog.com","-assets.i.posthog.com")+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e},u.people.toString=function(){return u.toString(1)+".people (stub)"},o="init capture register register_once register_for_session unregister unregister_for_session getFeatureFlag getFeatureFlagPayload isFeatureEnabled reloadFeatureFlags updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures on onFeatureFlags onSessionId getSurveys getActiveMatchingSurveys renderSurvey canRenderSurvey getNextSurveyStep identify setPersonProperties group resetGroups setPersonPropertiesForFlags resetPersonPropertiesForFlags setGroupPropertiesForFlags resetGroupPropertiesForFlags reset get_distinct_id getGroups get_session_id get_session_replay_url alias set_config startSessionRecording stopSessionRecording sessionRecordingStarted captureException loadToolbar get_property getSessionProperty createPersonProfile opt_in_capturing opt_out_capturing has_opted_in_capturing has_opted_out_capturing clear_opt_in_out_capturing debug".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);
    posthog.init('phc_79RpiYGOIeOrJuM1gdxQtT2aQHwltOyLPRd6V1ZrRq6', {api_host: 'https://us.i.posthog.com'})
</script>
</head>
"""


def inject_ga():
    index_path = pathlib.Path(st.__file__).parent / "static" / "index.html"
    soup = BeautifulSoup(index_path.read_text(), features="html.parser")
    if not soup.find(id=GA_ID): 
        bck_index = index_path.with_suffix('.bck')
        if bck_index.exists():
            shutil.copy(bck_index, index_path)  
        else:
            shutil.copy(index_path, bck_index)  
        
        html = str(soup)
        
        # Add all head content (analytics and SEO tags)
        new_html = html.replace('<head>', '<head>\n' + SEO_TAGS + GA_SCRIPT + PS_SCRIPT)
        
        # Add noscript after body tag
        new_html = new_html.replace('<body>', '<body>\n' + GA_NOSCRIPT)
        
        # Remove any existing title tag (to avoid duplicates)
        new_html = new_html.replace('<title>Streamlit</title>', '')
        
        index_path.write_text(new_html)

inject_ga()
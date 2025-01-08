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
<title>CalcThing - Visual Calculator for Engineering & Physics</title>
<meta name="description" content="Interactive visual calculator for engineering and physics. Calculate and visualize circuits, fluid mechanics, and more in real-time. Features include Wye-Delta conversion, voltage dividers, current dividers, and fluid dynamics calculations.">

<!-- Google AdSense -->
<meta name="google-adsense-account" content="ca-pub-6414688600235144">

<!-- Additional SEO meta tags -->
<meta name="keywords" content="visual calculator, engineering calculator, physics calculator, circuit calculator, fluid mechanics, wye-delta conversion, voltage divider, current divider, real-time visualization, engineering tools">
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
        new_html = html.replace('<head>', '<head>\n' + SEO_TAGS + GA_SCRIPT)
        
        # Add noscript after body tag
        new_html = new_html.replace('<body>', '<body>\n' + GA_NOSCRIPT)
        
        # Remove any existing title tag (to avoid duplicates)
        new_html = new_html.replace('<title>Streamlit</title>', '')
        
        index_path.write_text(new_html)

inject_ga()
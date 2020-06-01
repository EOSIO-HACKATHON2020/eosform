//some default pre init
var Countly = Countly || {};
Countly.q = Countly.q || [];

//provide countly initialization parameters
Countly.app_key = 'dc654d52bd0f1a5dedae22af3ace87f9e8e2840a';
Countly.url = 'https://countly.teeko.io';

Countly.q.push(['track_sessions']);
Countly.q.push(['track_pageview']);
Countly.q.push(['track_clicks']);
Countly.q.push(['track_scrolls']);
Countly.q.push(['track_errors']);
Countly.q.push(['track_links']);
Countly.q.push(['track_forms']);
Countly.q.push(['collect_from_forms']);

//load countly script asynchronously
(function() {
   var cly = document.createElement('script'); cly.type = 'text/javascript';
   cly.async = true;
   //enter url of script here
   cly.src = 'https://cdnjs.cloudflare.com/ajax/libs/countly-sdk-web/20.4.0/countly.min.js';
   cly.onload = function(){Countly.init()};
   var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(cly, s);
})();

document.title = 'Mutual Fund Compass';
const icon = document.createElement('link');
icon.rel = 'icon';
icon.href = 'favicon.png';
document.head.appendChild(icon);

const bar = document.createElement('header');
bar.className = 'site-bar';
bar.innerHTML = '<div><a class="site-brand" href="index.html"><img src="favicon.png" alt="">Mutual Fund Compass</a>'
  + '<nav><a href="index.html">All funds</a>'
  + '<a href="https://github.com/AvilPage/mutual-fund-compass" rel="noopener">GitHub</a></nav></div>';
document.body.insertBefore(bar, document.body.firstChild);

const footer = document.createElement('p');
footer.className = 'site-footer';
footer.textContent = 'Data from Kuvera and mfapi.in. For information only, not investment advice. '
  + 'Mutual fund investments are subject to market risks.';
document.body.appendChild(footer);

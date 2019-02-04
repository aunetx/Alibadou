var socket = io()
  , page = 0
  , pgMax = 15
  , painterPage = 14;

if (page == 0) {
  $('#leftPage').addClass('noVisible');
}
$('#menu #li' + page).addClass('menuPageOn');

socket.on('connected', function() {
  console.log('Real-time connection up');
});

function goToPage(pg) {
  if (pg == 'previous') {
    pg = page - 1;
  } else if (pg == 'next') {
    pg = page + 1;
  } else if (typeof(pg) == 'number') {
    pg = pg;
  }
  if (pg == painterPage) {

    $(".loader-wrapper").fadeIn('300', function() {
      content = document.getElementById('content');
      pageName = document.getElementById('pageName');
      pageName.textContent = 'Painter';
      while (content.firstChild) {
      content.removeChild(content.firstChild);
      }
      var iframe = document.createElement("iframe");
      var iframeArticle = document.createElement("article");
      iframe.setAttribute("src", "painter/painter.html");
      iframeArticle.classList.add('containFrame');
      content.appendChild(iframeArticle);
      iframeArticle.appendChild(iframe);
      page = painterPage;

      $('#menu li').removeClass('menuPageOn');
      $('#menu #li' + page).addClass('menuPageOn');
      $('#leftPage').removeClass('noVisible');
      $('#rightPage').removeClass('noVisible');

      $(iframe).on('load', function() {
        $(".loader-wrapper").fadeOut('1000');
      });
    });

  } else if (pg >= 0 && pg <= pgMax) {

    $(".loader-wrapper").fadeIn('300', function() {
      socket.emit('goToPage', pg);
    });
    console.log('Going to page ' + pg);
  }
  $('#menu').slideUp('fade');
  $('#showMenu').removeClass('stillHover');
}

socket.on('page', function(jsonPage) {
  var pageContent = jsonPage.content
    , pgName = jsonPage.name
    , pageNumber = jsonPage.number;
  content = document.getElementById('content');
  pageName = document.getElementById('pageName');
  content.innerHTML = pageContent;
  pageName.textContent = pgName;
  $('#menu li').removeClass('menuPageOn');
  page = jsonPage.number;
  $('#menu #li' + page).addClass('menuPageOn');
  $('#leftPage').removeClass('noVisible');
  $('#rightPage').removeClass('noVisible');
  if (page == 0) {
    $('#leftPage').addClass('noVisible');
  }
  if (page == 4) {
    initializeExp2();
  }
  if (page == pgMax) {
    $('#rightPage').addClass('noVisible');
  }
  console.log('Gone to page ' + page);
  setTimeout(function() {
    $(".loader-wrapper").fadeOut("1000");
  }, '200');
});

function showMenuList() {
  var width = document.getElementById('h2nav').getBoundingClientRect().width;
  $('#menu').width(width);
  $('#menu').slideToggle('fade');
  $('#showMenu').toggleClass('stillHover');
}

function initializeExp2() {
  chart_exp2 = echarts.init(document.getElementById('exp2-results'), null, {renderer: 'svg'});
  option = {
    xAxis: {
      type: 'category',
      name: 'Temps,\nen semaine',
      boundaryGap : false,
      data: [0, 0.6, 1, 1.5, 2, 3, 4, 5],
      axisLine: {
        lineStyle: {
          color: "#abb4ba"
        }
      },
      axisLabel: {
        textStyle: {
          color: "#abb4ba"
        }
      }
    },
    yAxis: {
      name: 'Nombre de séquences\nen 30 secondes',
      type: 'value',
      axisLine: {
        lineStyle: {
          color: "#abb4ba"
        }
      },
      axisLabel: {
        textStyle: {
          color: "#abb4ba"
        }
      }
    },
    series: [{
      data: [17, 24, 29, 33, 35, 37, 38, 38],
      type: 'line'
    }],
    color: ['#CB4D4D']
  };
  chart_exp2.setOption(option);
}

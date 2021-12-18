var sites = [
  "https://www.fabiocrameri.ch/colourmaps/",
  "https://colorhunt.co/",
  "https://krischer.github.io/seismo_live_build/",
  "https://complexityexplained.github.io/",
  "https://www.complexity-explorables.org/",
  "https://github.com/matplotlib/cheatsheets/",
  "https://gfarge.github.io/the-void/index.html",
  "https://vimeo.com/seismicsoundlab",
  "https://seismicsoundlab.github.io/",
  "https://www.imdb.com/title/tt0318997/",
  "https://www.imdb.com/title/tt5687612/",
  "https://www.imdb.com/title/tt7660850/",
  "https://www.youtube.com/c/ChineseCookingDemystified",
  "https://www.youtube.com/channel/UCLXDNUOO3EQ80VmD9nQBHPg",
  "https://www.youtube.com/channel/UC9owMb8geiOVPSQdr6EtGnA",
  "https://www.youtube.com/channel/UCMFcMhePnH4onVHt2-ItPZw",
  "https://www.youtube.com/channel/UCvjgXvBlbQiydffZU7m1_aw",
    ];

    function randomSite() {
        var i = parseInt(Math.random() * sites.length);
        location.href = sites[i];
    }

(() => {
  const input = document.querySelector("#library-search");
  if (!input) return;

  const results = document.querySelector("#search-results");
  const browse = document.querySelector("#browse-list");
  const status = document.querySelector("#search-status");
  let documents = [];

  fetch(`${document.documentElement.dataset.baseurl || ""}/search.json`)
    .then((response) => {
      if (!response.ok) throw new Error("Search index unavailable");
      return response.json();
    })
    .then((data) => { documents = data; })
    .catch(() => { status.textContent = "Search is temporarily unavailable."; });

  const escapeHtml = (value) => value.replace(/[&<>'"]/g, (character) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;"
  })[character]);

  input.addEventListener("input", () => {
    const query = input.value.trim().toLocaleLowerCase();
    if (query.length < 2) {
      results.hidden = true;
      browse.hidden = false;
      results.innerHTML = "";
      status.textContent = "";
      return;
    }

    const matches = documents.filter((document) =>
      `${document.title} ${document.description} ${document.category}`.toLocaleLowerCase().includes(query)
    );
    results.innerHTML = matches.map((document) => `
      <a class="article-row" href="${encodeURI(document.url)}">
        <span><strong>${escapeHtml(document.title)}</strong><small>${escapeHtml(document.category)} — ${escapeHtml(document.description)}</small></span>
        <span class="arrow" aria-hidden="true">&rarr;</span>
      </a>`).join("");
    results.hidden = false;
    browse.hidden = true;
    status.textContent = `${matches.length} document${matches.length === 1 ? "" : "s"} found`;
  });
})();


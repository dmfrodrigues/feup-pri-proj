function formatDate(d){
    if(d == undefined || d == '') return d
    const date = new Date(d)
    return `${date.getFullYear().toString()}/${(date.getMonth()+1).toString().padStart(2, '0')}/${date.getDate().toString().padStart(2, '0')}`;
}

function formatList(l) {
    if(l == undefined) return "";
    l = l[0];
    if(l.length <= 0) return "";
    return l.split(';').map(t => `<span class="tag">${t}</span>`).join('');
}

function updateBoardData(dataObj, page){
    const board = document.getElementById('board')
    board.innerHTML = ''

    const docs = dataObj.response.docs
    
    let i = 1
    for(const doc of docs){
        const div = document.createElement('div')
        div.classList = "doc-div"
        div.id = doc.celex
        div.innerHTML = `
            <details>
                <summary>
                    <div class="id">
                        <tt>${doc.celex}</tt>
                    </div>
                    <div class="title">
                        ${doc.title}
                    </div>
                </summary>
                <div class="search-result">
                    <div class="search-result-metadata">
                        <table>
                            <tr><th>Date</th>           <td>${formatDate(doc["date"])}</td></tr>
                            <tr><th>OJ date</th>        <td>${formatDate(doc["oj_date"])}</td></tr>
                            <tr><th>Of effect</th>      <td>${formatDate(doc["of_effect"])}</td></tr>
                            <tr><th>End validity</th>   <td>${formatDate(doc["end_validity"])}</td></tr>
                            <tr><th>Subject matter</th> <td><div class="flex-wrap">${formatList(doc.subject_matter      )}</div></td></tr>
                            <tr><th>Directory codes</th><td><div class="flex-wrap">${formatList(doc.directory_codes     )}</div></td></tr>
                            <tr><th>EuroVoc</th>        <td><div class="flex-wrap">${formatList(doc.eurovoc_descriptors )}</div></td></tr>
                            <tr><th>Legal basis</th>    <td><div class="flex-wrap">${formatList(doc.legal_basis         )}</div></td></tr>
                            <tr><th>Relationships</th>  <td><div class="flex-wrap">${formatList(doc.relationships       )}</div></td></tr>
                        </table>
                    </div>
                    <iframe class="search-result-body" src="/eurlex/legal-content/EN/TXT/HTML/?celex=${doc.celex}">
                    </iframe>
                </div>
            </details>
        `
        
        board.appendChild(div)

        i += 1
    }
}

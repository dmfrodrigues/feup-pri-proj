var q_facetQuery = ''
var q_facetFilter = ''

function getFacetCheckboxes(){
    return document.getElementById('faceting').faceting
}

function facetQuery(checkboxes_nodelist = getFacetCheckboxes()){
    let facet_checkboxes = Array.from(checkboxes_nodelist)

    if (facet_checkboxes.length == 0 || 
        facet_checkboxes.every(checkbox => !checkbox.checked)) return ""

    let result = 
        "&facet=true" +
        "&facet.sort=count"
    
    for (let checkbox of facet_checkboxes){
        if (checkbox.checked)
        result += "&facet.field=" + checkbox.defaultValue
    }

    return result
}

var active_tab = false
function updateFacetingResults(request){
    let tabDiv = document.getElementById('faceting-results-tab')
    tabDiv.firstElementChild.innerHTML = ''
    while (tabDiv.lastChild.className != 'tab')
        tabDiv.removeChild(tabDiv.lastChild)

    if (!request.facet_counts) return

    let fields = request.facet_counts.facet_fields
    for (let field in fields){
        let newTab = document.createElement('button')
        newTab.className = 'tablink'
        newTab.innerHTML = field
        newTab.setAttribute('onclick', 'clickFacetingField(event)')

        let newContent = document.createElement('ul')
        newContent.id = field
        newContent.className = "tabcontent"

        i = -1
        let newEntry
        for(let entry of fields[field]){
            i++
            if (i % 2){ // Entry is value
                if (entry == '0') continue

                newEntry.innerHTML+=` (${entry})`
                newContent.appendChild(newEntry)
            }
            else{ // Entry is name
                newEntry = document.createElement('li')
                newEntry.innerHTML = `<b>${entry}</b>`
                newEntry.setAttribute('onclick', `clickFacetingEntry('${field}', '${entry}')`)
            }
        }
        if (newContent.childNodes.length > 1){
            tabDiv.appendChild(newContent)
            tabDiv.firstElementChild.appendChild(newTab)
        }
    }

    if (active_tab){
        clickFacetingField({currentTarget:active_tab})
    }
}

function clickFacetingField(event){
    console.log(active_tab)
    let tabContents = document.getElementsByClassName('tabcontent')
    for (let tab of tabContents) tab.style.display = 'none'

    let tabLinks = document.getElementsByClassName('tablink')
    for (let link of tabLinks) link.className = link.className.replace('active', '')
    
    document.getElementById(event.currentTarget.innerHTML).style.display = 'block'
    event.currentTarget.className += " active"

    active_tab = event.currentTarget
}
function clickFacetingEntry(field, entry){
    q_facetFilter = `&fq={!raw f=${field}}${entry}`
    this.runQuery()
}

var q_facetQuery = ''
var q_facetFilter = {}

function getFacetFieldsCheckboxes(){
    return document.getElementById('faceting').faceting
}
function getFacetValuesCheckboxes(name){
    return document.getElementById(name).children
}

function facetQuery(checkboxes_nodelist = getFacetFieldsCheckboxes()){
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
            
            if (!(i % 2)){ // Entry is name
                // Special case for 'empty' value
                if (entry == "#") entry = 'None'

                newEntry = document.createElement('li')
                newEntry.innerHTML = 
                    `<label>
                        <input type="checkbox" onChange="updateFacetFilter(this.checked, '${field}', '${entry}')" name="faceting" value="">
                        <b>${entry}`
            }
            else{ // Entry is value
                if (entry == '0') continue

                let entryIsEmpty = newEntry.innerHTML.includes("None")
                newEntry.innerHTML+=` (${entry})</b></label>`
                if (entryIsEmpty){
                    newContent.insertBefore(newEntry, newContent.firstChild)
                }
                else
                    newContent.appendChild(newEntry)
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

function checkForNone(checked, field, entry){
    if (entry != "None") return
    
    let siblingCheckboxes = Array.from(document.querySelectorAll(`#${field} input`)).slice(1)
    for (let checkbox of siblingCheckboxes)
        checkbox.disabled = checked
}

function clickFacetingField(event){
    let tabContents = document.getElementsByClassName('tabcontent')
    for (let tab of tabContents) tab.style.display = 'none'

    let tabLinks = document.getElementsByClassName('tablink')
    for (let link of tabLinks) link.className = link.className.replace('active', '')
    
    let tabContent = document.getElementById(event.currentTarget.innerHTML)
    if (!tabContent) return
    tabContent.style.display = 'block'
    event.currentTarget.className += " active"

    active_tab = event.currentTarget
}
function updateFacetFilter(checked, field, entry){
    checkForNone(checked, field, entry)
    let entryWords = entry.split(' ')
    entry = entryWords.length>1? entryWords.join('*'):entry

    let fieldSet = q_facetFilter[field]
    if (fieldSet){
        if (checked)
            fieldSet.add(entry)
        else
            fieldSet.delete(entry)
    }
    else if (checked) q_facetFilter[field] = new Set([entry])

    facetAndSearch(false)
}
function formatFacetFilter(){
    let result = []
    for (let field in q_facetFilter){
        // Special case for 'empty' val
        if (q_facetFilter[field].has('None')){
            result.push(`-${field}:[* TO *]`)
        }
        else {
            let val = Array.from(q_facetFilter[field])
            if (val.length)
                result.push(`${field}:(${val.join(' AND ')})`)   
        }
    }

    return '&fq=' + result.join(' AND ')
}
function toggle(id) {
    tbl = document.getElementById(id);
    if (tbl.style.display == 'none')
        tbl.style.display = 'block';
    else
        tbl.style.display = 'none';
}

function addElement(cb, table, clm) {
    var ele = document.getElementById('div-' + table + '.' + clm);
    if (cb.checked == true)
        ele.style.display = 'inline-block';
    else
        ele.style.display = 'none';
}

function addElement2(table, clm) {
    var sheet = document.getElementById('sheet');
    var fieldtemplate = document.getElementById('fieldtemplate');
    var frag = document.createDocumentFragment(),
        temp = document.createElement('div');
    temp.innerHTML = fieldtemplate.innerHTML;
    while (temp.firstChild) {
        frag.appendChild(temp.firstChild);
    }
    sheet.appendChild(frag);
}
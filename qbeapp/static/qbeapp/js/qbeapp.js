function toggle(id) {
    tbl = document.getElementById(id);
    if (tbl.style.display == 'none')
        tbl.style.display = 'block';
    else
        tbl.style.display = 'none';
}

function addElement(cb, table, clm) {
    var el_form = document.getElementById('div-' + table + '.' + clm);
    var cnt = document.getElementById('cnt-' + table + '.' + clm).value;
    var hid_id = 'id_' + 'form-' + cnt + '-field'
    var el_hid = document.getElementById(hid_id)
    if (cb.checked == true) {
        el_form.style.display = 'inline-block';
        el_hid.value = table + '.' + clm;
    } else {
        el_form.style.display = 'none';
        el_hid.value = '';
    }
}
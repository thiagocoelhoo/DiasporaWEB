function submitFormAsync(form, refresh=false){
    let fields = form.querySelectorAll("input,textarea");
    let data = new URLSearchParams();

    for (let i = 0; i < fields.length; i++) {
        let field = fields[i];
        data.append(field.name, field.value);
    }

    fetch(form.attributes.action.value, {
        method: 'post',
        body: data
    })
    .then(function (response) {
        console.log(response.text());
        document.location.reload(true);
    })
    
    return false;
}

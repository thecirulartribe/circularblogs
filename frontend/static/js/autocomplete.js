new Autocomplete('#autocomplete', {
    search : input => {
    const url = `/get_blog/?search=${input}`
    return new Promise(resolve => {
    fetch(url)
    .then(response => response.json())
    .then(data => {
    resolve(data.payload)
    })
    })
    }
})

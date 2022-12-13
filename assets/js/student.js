const semesterChoice = document.getElementById("semester")

const forms = document.getElementsByTagName("form")

displaySemester()

semesterChoice.addEventListener("click", () => {
    displaySemester()
})

Array.from(forms).forEach(form => {
    form.addEventListener("click", form => {
        form.submit()
    })
})

function displaySemester() {
    Array.from(semesterChoice.options).forEach(option => {
        let value = option.value
        const currentSemester = document.getElementsByClassName(value)[0]
        if (currentSemester == undefined)
            return
        if (option.selected)
            currentSemester.style.display = "flex"
        else
            currentSemester.style.display = "none"
        return
    })
}
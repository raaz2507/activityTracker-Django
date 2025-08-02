document.addEventListener("DOMContentLoaded", () => {
    const yearInput = document.getElementById("yearInput");

    yearInput.addEventListener("change", () => {
        console.log(yearInput.value)
        const year = parseInt(yearInput.value);
        if (!isNaN(year) && year >= 1000 && year <= 9999) {
        window.location.href = calendarURL.replace("0", year);
        }
    });
});


// its for marking but now its doing  in view 
// document.addEventListener('DOMContentLoaded', () => {
//     markedData.forEach((month, index) => {
//       const dayCells = document.querySelectorAll(`table:nth-of-type(${index + 1}) td`);
//       month.marked_days.forEach(day => {
//         console.log(`day got ${day}`);
//         dayCells.forEach(td => {
//           if (
//             td.innerText.trim() === day.toString() 
//             // &&
//             // td.closest('table').querySelector('caption').textContent.includes(month.name)
//           ) {
//             console.log(td);
//             td.classList.add('marked-day');
//           }
//         });
//       });
//     });
//   });

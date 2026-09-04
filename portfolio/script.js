document.addEventListener('DOMContentLoaded', () => {
  // Category Filter Logic
  const filterBtns = document.querySelectorAll('.filter-btn');
  const tableRows = document.querySelectorAll('.tech-table tbody tr');

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const filter = btn.getAttribute('data-filter');

      tableRows.forEach(row => {
        const rowCat = row.getAttribute('data-cat');
        if (filter === 'all' || rowCat === filter || rowCat === 'all') {
          row.style.display = '';
        } else {
          row.style.display = 'none';
        }
      });
    });
  });

  // Email quick copy handler
  const emailBtn = document.getElementById('email-btn');
  if (emailBtn) {
    emailBtn.addEventListener('click', (e) => {
      // Let mailto work normally, but show tooltip or alert
      console.log('Email link clicked: naveenbjvn8050@gmail.com');
    });
  }
});

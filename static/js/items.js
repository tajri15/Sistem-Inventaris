// static/js/items.js

document.addEventListener('DOMContentLoaded', function() {
    const itemForm = document.getElementById('itemForm');
    const itemModal = new bootstrap.Modal(document.getElementById('itemModal'));

    itemForm.addEventListener('submit', function(event) {
        // Hentikan proses submit form standar yang me-reload halaman
        event.preventDefault();

        const formData = new FormData(itemForm);
        const url = itemForm.action;

        fetch(url, {
            method: 'POST',
            body: formData,
            headers: {
                // Header ini memberitahu backend bahwa ini adalah request AJAX
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Jika sukses, tambahkan baris baru ke tabel
                const tableBody = document.getElementById('items-table-body');
                const newRow = createTableRow(data.item);
                tableBody.insertAdjacentHTML('afterbegin', newRow);
                
                // Tutup modal dan tampilkan notifikasi
                itemModal.hide();
                alert(data.message); // Anda bisa ganti dengan notifikasi yang lebih cantik
            } else {
                // Jika gagal, tampilkan error
                alert('Error: ' + Object.values(data.errors).join('\n'));
            }
        })
        .catch(error => {
            console.error('Submission failed:', error);
            alert('An unexpected error occurred.');
        });
    });
});

// Fungsi bantuan untuk membuat baris tabel baru
function createTableRow(item) {
    // Sesuaikan HTML ini agar sama persis dengan struktur <tr> di items.html Anda
    return `
        <tr>
            <td><strong>${item.code}</strong></td>
            <td><strong>${item.name}</strong></td>
            <td><span class="badge bg-info">${item.category}</span></td>
            <td><span class="badge bg-success">${item.quantity}</span></td>
            <td>${item.unit_price}</td>
            <td>${item.supplier}</td>
            <td><small>${item.created_at}</small></td>
            <td>
                <div class="btn-group btn-group-sm" role="group">
                    <a href="/items/edit/${item.id}" class="btn btn-outline-warning">
                        <i class="fas fa-edit"></i>
                    </a>
                    <button type="button" class="btn btn-outline-danger" onclick="confirmDelete(${item.id}, '${item.name}')">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </td>
        </tr>
    `;
}
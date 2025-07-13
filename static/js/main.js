// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('PT Telkom Indonesia Inventory System initialized successfully!');
    
    // Initialize sidebar functionality
    initializeSidebar();
    
    // Initialize stock status checking
    updateStockStatus();
});

// Sidebar functionality
function initializeSidebar() {
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebarClose = document.getElementById('sidebarClose');
    const sidebar = document.getElementById('sidebar');
    
    // Open sidebar
    function openSidebar() {
        sidebar.classList.add('show');
        // Tambahkan class ke body untuk memicu pergeseran konten
        document.body.classList.add('sidebar-open');
    }
    
    // Close sidebar
    function closeSidebar() {
        sidebar.classList.remove('show');
        // Hapus class dari body untuk mengembalikan posisi konten
        document.body.classList.remove('sidebar-open');
    }
    
    // Event listeners
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', openSidebar);
    }
    
    if (sidebarClose) {
        sidebarClose.addEventListener('click', closeSidebar);
    }

    // Close sidebar on escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && sidebar.classList.contains('show')) {
            closeSidebar();
        }
    });
}

// Function to update stock status indicators
function updateStockStatus() {
    const stockBadges = document.querySelectorAll('[data-stock-level]');
    
    stockBadges.forEach(badge => {
        const stockLevel = parseInt(badge.dataset.stockLevel);
        const minStock = parseInt(badge.dataset.minStock) || 10;
        
        function checkStock() {
            if (stockLevel === 0) {
                badge.className = 'badge bg-danger';
                badge.textContent = 'Out of Stock';
            } else if (stockLevel <= minStock) {
                badge.className = 'badge bg-warning';
                badge.textContent = 'Low Stock';
            } else {
                badge.className = 'badge bg-success';
                badge.textContent = 'In Stock';
            }
        }
        
        checkStock();
    });
}
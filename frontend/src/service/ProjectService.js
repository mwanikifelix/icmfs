export const ProjectService = {
    getProjectsData() {
        return [
            {
                id: 'P-001',
                code: 'MSA-AHP-001',
                name: 'Affordable Housing – Mombasa',
                description: 'Government affordable housing project',
                image: 'project-mombasa.jpg',
                price: 250000000,
                category: 'Residential',
                quantity: 120, // housing units
                inventoryStatus: 'ONGOING',
                rating: 4
            },
            {
                id: 'P-002',
                code: 'NRB-AHP-014',
                name: 'Affordable Housing – Nairobi',
                description: 'Multi-site urban housing development',
                image: 'project-nairobi.jpg',
                price: 520000000,
                category: 'Residential',
                quantity: 300,
                inventoryStatus: 'PLANNING',
                rating: 5
            },
            {
                id: 'P-003',
                code: 'KSM-INF-007',
                name: 'Infrastructure Upgrade – Kisumu',
                description: 'Road & drainage infrastructure works',
                image: 'project-kisumu.jpg',
                price: 180000000,
                category: 'Infrastructure',
                quantity: 45,
                inventoryStatus: 'ONHOLD',
                rating: 3
            }
        ];
    },

    getProjectsWithOrdersData() {
        return [
            {
                id: 'P-001',
                code: 'MSA-AHP-001',
                name: 'Affordable Housing – Mombasa',
                description: 'Government affordable housing project',
                image: 'project-mombasa.jpg',
                price: 250000000,
                category: 'Residential',
                quantity: 120,
                inventoryStatus: 'ONGOING',
                rating: 4,
                orders: [
                    {
                        id: 'PO-001',
                        productCode: 'MSA-AHP-001',
                        date: '2025-01-12',
                        amount: 45000000,
                        quantity: 500,
                        customer: 'Bamburi Cement Ltd',
                        status: 'DELIVERED'
                    },
                    {
                        id: 'PO-002',
                        productCode: 'MSA-AHP-001',
                        date: '2025-02-03',
                        amount: 18000000,
                        quantity: 200,
                        customer: 'Devki Steel Mills',
                        status: 'PENDING'
                    }
                ]
            }
        ];
    },

    getProjectsMini() {
        return Promise.resolve(this.getProjectsData().slice(0, 5));
    },

    getProjectsSmall() {
        return Promise.resolve(this.getProjectsData().slice(0, 10));
    },

    getProjects() {
        return Promise.resolve(this.getProjectsData());
    },

    getProjectsWithOrdersSmall() {
        return Promise.resolve(this.getProjectsWithOrdersData().slice(0, 10));
    },

    getProjectsWithOrders() {
        return Promise.resolve(this.getProjectsWithOrdersData());
    }
};

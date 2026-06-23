document.addEventListener('DOMContentLoaded', async () => {
    // Use relative paths on Railway/localhost, but absolute URL on Vercel
    const API_BASE_URL = window.location.hostname.includes('vercel.app')
        ? 'https://web-production-05719.up.railway.app' // Correct Railway URL for Vercel
        : '';

    const form = document.getElementById('recommendationForm');
    const resultsContainer = document.getElementById('resultsContainer');
    const emptyState = document.getElementById('emptyState');
    const loadingState = document.getElementById('loadingState');
    const locationInput = document.getElementById('locationInput');

    try {
        const locResponse = await fetch(`${API_BASE_URL}/locations`);
        const locData = await locResponse.json();
        if (locData.status === 'success' && locData.data) {
            const defaultOption = '<option value="" disabled selected>Select Location</option>';
            const options = locData.data.map(loc => `<option value="${loc}">${loc}</option>`).join('');
            locationInput.innerHTML = defaultOption + options;
        }
    } catch (e) {
        console.error("Failed to load locations", e);
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Get values
        const location = document.getElementById('locationInput').value;
        const budget = document.getElementById('budgetInput').value;
        const cuisine = document.getElementById('cuisineInput').value;
        const ratingStr = document.getElementById('ratingInput').value;
        const minRating = ratingStr ? parseFloat(ratingStr) : 0.0;
        const additionalPreferences = document.getElementById('additionalPreferences').value;

        // Hide empty state and any previous results
        resultsContainer.innerHTML = '';
        resultsContainer.style.display = 'none';
        emptyState.style.display = 'none';

        // Show loader
        loadingState.classList.remove('hidden');
        loadingState.classList.add('flex');

        try {
            const response = await fetch(`${API_BASE_URL}/recommend`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    location: location,
                    budget: budget,
                    cuisine: cuisine,
                    min_rating: minRating,
                    additional_preferences: additionalPreferences
                })
            });

            const data = await response.json();

            // Hide loader
            loadingState.classList.add('hidden');
            loadingState.classList.remove('flex');

            if (data.status === 'success' || data.status === 'partial_success') {
                renderResults(data);
                resultsContainer.style.display = 'block';
            } else {
                renderError(data.message || 'An error occurred. Please try again.');
                resultsContainer.style.display = 'block';
            }

        } catch (error) {
            console.error('Error fetching recommendations:', error);
            loadingState.classList.add('hidden');
            loadingState.classList.remove('flex');
            renderError('Failed to connect to the server. Please ensure the backend is running.');
            resultsContainer.style.display = 'block';
        }
    });

    function renderResults(responseJson) {
        let content = '';

        if (!responseJson.data || (Array.isArray(responseJson.data) && responseJson.data.length === 0) || (responseJson.data.recommendations && responseJson.data.recommendations.length === 0)) {
            content = `
                <div class="text-center text-on-surface-variant py-10">
                    <span class="material-symbols-outlined text-[64px] text-error mb-2">sentiment_dissatisfied</span>
                    <h2 class="text-xl font-bold text-on-surface mb-2">No Matches Found</h2>
                    <p class="text-md">${responseJson.message || 'We could not find any restaurants matching your exact criteria. Try adjusting your filters.'}</p>
                </div>
            `;
            resultsContainer.innerHTML = content;
            return;
        }

        // Handle both LLM success and partial success (fallback)
        const isFallback = Array.isArray(responseJson.data);
        const recommendations = isFallback ? responseJson.data : responseJson.data.recommendations;
        const summary = isFallback ? responseJson.message : responseJson.data.summary;

        if (summary) {
            content += `
                <!-- AI Summary Banner -->
                <div class="bg-primary/5 border border-primary/20 rounded-xl p-6 flex gap-4 items-start shadow-sm mb-6">
                    <div class="text-primary mt-1">
                        <span class="material-symbols-outlined text-[32px]" style="font-variation-settings: 'FILL' 1;">auto_awesome</span>
                    </div>
                    <div>
                        <h2 class="font-headline-md text-headline-md text-on-surface mb-2">Curated for You</h2>
                        <p class="font-body-md text-body-md text-on-surface-variant leading-relaxed">
                            ${summary}
                        </p>
                    </div>
                </div>
            `;
        }

        content += '<div class="space-y-6">';

        recommendations.forEach((rec, index) => {
            // For fallback, field names might be 'name' instead of 'restaurant_name' and missing 'explanation'
            const name = rec.restaurant_name || rec.name || 'Unknown Restaurant';
            const cost = rec.estimated_cost || rec.cost || 'N/A';
            const rating = rec.rating ? parseFloat(rec.rating).toFixed(1) : 'N/A';
            const cuisines = rec.cuisine || rec.cuisines || 'Various';
            const explanation = rec.explanation || 'Matches your criteria based on basic filtering.';

            // Since we removed images, the card layout expands beautifully
            content += `
                <!-- Card -->
                <div class="bg-surface-container-lowest rounded-xl shadow-ambient border border-outline-variant hover:shadow-[0px_16px_40px_rgba(0,0,0,0.08)] hover:-translate-y-0.5 transition-all duration-300 flex flex-col group p-6">
                    <div class="flex justify-between items-start mb-2">
                        <h3 class="font-headline-md text-headline-md text-on-surface font-semibold text-2xl">${name}</h3>
                        <button class="text-secondary hover:text-primary transition-colors"><span class="material-symbols-outlined">bookmark_border</span></button>
                    </div>
                    <div class="flex items-center flex-wrap gap-2 mb-4">
                        <div class="flex items-center text-primary text-sm bg-primary/10 px-2 py-1 rounded-md">
                            <span class="material-symbols-outlined text-[16px]" style="font-variation-settings: 'FILL' 1;">star</span>
                            <span class="font-semibold ml-1">${rating}</span>
                        </div>
                        <span class="text-secondary text-sm">•</span>
                        <span class="font-label-sm text-label-sm text-on-surface-variant bg-surface px-2 py-1 rounded-md border border-outline-variant">₹${cost} for two</span>
                        <span class="text-secondary text-sm">•</span>
                        <span class="font-label-sm text-label-sm text-on-surface-variant bg-surface px-2 py-1 rounded-md border border-outline-variant">${cuisines}</span>
                    </div>
                    
                    <div class="mt-2 bg-primary/5 rounded-lg p-4 border border-primary/10 flex-1">
                        <div class="flex items-center gap-2 mb-2">
                            <span class="material-symbols-outlined text-primary text-[18px]" style="font-variation-settings: 'FILL' 1;">auto_awesome</span>
                            <span class="font-label-sm text-label-sm text-primary uppercase tracking-widest font-bold">Why it matches</span>
                        </div>
                        <p class="font-body-md text-body-md text-on-surface-variant leading-relaxed">${explanation}</p>
                    </div>
                </div>
            `;
        });

        content += '</div>';
        resultsContainer.innerHTML = content;
    }

    function renderError(message) {
        resultsContainer.innerHTML = `
            <div class="bg-error-container text-on-error-container border border-error/20 rounded-xl p-6 flex gap-4 items-start shadow-sm mb-6">
                <div class="mt-1">
                    <span class="material-symbols-outlined text-[32px] text-error">error</span>
                </div>
                <div>
                    <h2 class="font-headline-md text-headline-md font-bold mb-2">Something went wrong</h2>
                    <p class="font-body-md text-body-md leading-relaxed">
                        ${message}
                    </p>
                </div>
            </div>
        `;
    }
});

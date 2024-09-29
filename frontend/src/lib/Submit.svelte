<script lang="ts">
    export let forest: Array<Array<number>> = [];

    async function forestPOST() {
        const URL = 'https://your-backend-url.com/submit-forest';
        
        try {
            const response = await fetch(URL, {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json',
                },
                body: JSON.stringify({ forest }),
            });

            if (!response.ok) {
                throw new Error('Network response invalid');
            }

            const result = await response.json();
            console.log('Forest submitted successfully:', result);
            alert('Forest Submitted!');
        } catch (error) {
            console.error('Error submitting forest:', error);
            alert('Error submitting forest. Please try again.');
        }
    }
</script>

<div>
    <button class="rounded-xl cursor-pointer" on:click={forestPOST}>Submit Forest</button>
</div>
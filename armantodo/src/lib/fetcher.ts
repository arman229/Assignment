export const fetcher = async (url: string) => {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Failed to fetch data');
        }
        const data = await response.json();
        return data;
    } catch (error: any) {
        throw new Error(error.message || 'An unexpected error occurred');
    }
};
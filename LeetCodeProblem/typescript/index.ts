function twoSum(nums: number[], target): number[] {
    // Create a map to store the number and its index
    const num_to_index: { [key: number]: number } = {};
    
    // Iterate through the array
    for (let i = 0; i < nums.length; i++) {
        const num = nums[i];
        const complement = target - num;
        
        // Check if the complement exists in the map
        if (num_to_index.hasOwnProperty(complement)) {
            // Return the indices of the complement and the current number
            return [num_to_index[complement], i];
        }
        
        // Add the current number and its index to the map
        num_to_index[num] = i;
    }
    
    // Return an empty array if no solution is found (shouldn't happen as per problem constraints)
    return [];
}
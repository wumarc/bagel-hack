// Navbar title click redirect to index.html
document.addEventListener('DOMContentLoaded', function() {
    const eventTitle = document.getElementById('navTitle');
    
    if (eventTitle) {
        eventTitle.style.cursor = 'pointer';
        eventTitle.addEventListener('click', function() {
            window.location.href = 'index.html';
        });
    }
});


function generateEventRecommendations() {
    // Generate event recommendations based on user profile
    const profession = userProfile.profession.toLowerCase();
    const interests = userProfile.interests.toLowerCase();
    const location = userProfile.location.toLowerCase();
    
    // Industry-specific events
    if (profession.includes("tech") || profession.includes("software") || profession.includes("developer") || 
        interests.includes("tech") || interests.includes("software") || interests.includes("programming")) {
        
        addBotMessage(`1. ${location.includes("virtual") ? "Virtual" : ""} Tech Connect Summit - A gathering of technology professionals discussing the latest industry trends. Perfect for networking with tech leaders and innovators.`);
        
        addBotMessage(`2. ${location.includes("virtual") ? "Online" : "Local"} Developer Meetup - Monthly casual gatherings for developers to exchange ideas and build professional connections.`);
        
    } else if (profession.includes("finance") || profession.includes("banking") || 
              interests.includes("finance") || interests.includes("investment")) {
        
        addBotMessage(`1. Financial Professionals Networking Forum - An exclusive ${location.includes("virtual") ? "virtual" : "in-person"} event for finance industry leaders to connect and discuss market trends.`);
        
        addBotMessage(`2. Investment Strategies Roundtable - A focused networking event with presentations and dedicated networking sessions.`);
        
    } else if (profession.includes("market") || profession.includes("sales") || 
              interests.includes("market") || interests.includes("digital market")) {
        
        addBotMessage(`1. Marketing Innovators Conference - Connect with creative marketing professionals and industry pioneers in ${location}.`);
        
        addBotMessage(`2. Sales & Marketing Professionals Mixer - Monthly networking events focused on relationship building and lead generation strategies.`);
        
    } else {
        // Generic recommendations based on location
        addBotMessage(`1. Professional Networking Association Meetup in ${location} - Regular events bringing together professionals from diverse backgrounds.`);
        
        addBotMessage(`2. Industry Insights Conference - A major ${location.includes("virtual") ? "virtual" : "in-person"} event with keynote speakers and structured networking sessions.`);
    }
    
    // Universal recommendation
    addBotMessage(`3. Cross-Industry Networking Event - Connect with professionals from various fields to expand your network beyond your immediate industry. ${location.includes("virtual") ? "Hosted virtually with breakout rooms for focused conversations." : "Features speed networking and open discussion forums."}`);
}


function generateSummary() {
    // Create and display summary
    const summaryMessage = `
Here's a summary of your networking preferences:

• Profession/Industry: ${userProfile.profession}
• Professional Interests: ${userProfile.interests}
• Experience Level: ${userProfile.experience}
• Preferred Location: ${userProfile.location}
${userProfile.additionalInfo && userProfile.additionalInfo !== "No additional preferences specified." ? "• Additional Preferences: " + userProfile.additionalInfo : ""}

I'll use this information to find the best networking events for you to connect with relevant professionals. Is there anything you'd like to change before I proceed?`;
    
    addBotMessage(summaryMessage);
    
    // Add follow-up message
    setTimeout(() => {
        addBotMessage("If everything looks good, I'll find networking events that match your criteria so you can start building valuable connections.");
    }, 2000);
}

// Navbar title click redirect to index.html
document.addEventListener('DOMContentLoaded', function() {
    const eventTitle = document.getElementById('navTitle');
    
    if (eventTitle) {
        eventTitle.style.cursor = 'pointer';
        eventTitle.addEventListener('click', function() {
            window.location.href = 'index.html';
        });
    }

    // Check if we're on the relevant-events page and populate it
    if (window.location.pathname.includes('relevant-events.html')) {
        populateRelevantEvents();
    }
});

// Modified function to return event objects instead of adding bot messages
function generateEventRecommendations(userProfile) {
    // Get user profile from sessionStorage if not provided
    if (!userProfile) {
        const storedProfile = sessionStorage.getItem('userProfile');
        if (storedProfile) {
            userProfile = JSON.parse(storedProfile);
        } else {
            // Default values if no profile exists
            userProfile = {
                profession: "technology",
                interests: "software development",
                experience: "5 years",
                location: "San Francisco"
            };
        }
    }
    
    // Get data from user profile
    const profession = userProfile.profession.toLowerCase();
    const interests = userProfile.interests.toLowerCase();
    const location = userProfile.location.toLowerCase();
    
    // Array to store event objects
    const events = [];
    
    // Industry-specific events
    if (profession.includes("tech") || profession.includes("software") || profession.includes("developer") || 
        interests.includes("tech") || interests.includes("software") || interests.includes("programming")) {
        
        events.push({
            title: "Tech Connect Summit",
            date: "March 15, 2024",
            summary: "A gathering of technology professionals discussing the latest industry trends. Perfect for networking with tech leaders and innovators.",
            location: `${location.includes("virtual") ? "Virtual Event" : "Silicon Valley Convention Center"}`,
            demographics: { tech: 90, art: 10 }
        });
        
        events.push({
            title: `${location.includes("virtual") ? "Online" : "Local"} Developer Meetup`,
            date: "March 20, 2024",
            summary: "Monthly casual gatherings for developers to exchange ideas and build professional connections.",
            location: `${location.includes("virtual") ? "Zoom Meeting" : "Innovation Hub Downtown"}`,
            demographics: { tech: 95, art: 5 }
        });
        
    } else if (profession.includes("finance") || profession.includes("banking") || 
              interests.includes("finance") || interests.includes("investment")) {
        
        events.push({
            title: "Financial Professionals Networking Forum",
            date: "April 5, 2024",
            summary: `An exclusive ${location.includes("virtual") ? "virtual" : "in-person"} event for finance industry leaders to connect and discuss market trends.`,
            location: `${location.includes("virtual") ? "Virtual Event" : "Financial District Conference Center"}`,
            demographics: { finance: 80, tech: 20 }
        });
        
        events.push({
            title: "Investment Strategies Roundtable",
            date: "April 12, 2024",
            summary: "A focused networking event with presentations and dedicated networking sessions.",
            location: `${location.includes("virtual") ? "Virtual Event" : "Capital Investments Building"}`,
            demographics: { finance: 85, business: 15 }
        });
        
    } else if (profession.includes("market") || profession.includes("sales") || 
              interests.includes("market") || interests.includes("digital market")) {
        
        events.push({
            title: "Marketing Innovators Conference",
            date: "March 22, 2024",
            summary: `Connect with creative marketing professionals and industry pioneers in ${location}.`,
            location: `${location.includes("virtual") ? "Virtual Event" : "Downtown Marketing Center"}`,
            demographics: { marketing: 70, tech: 30 }
        });
        
        events.push({
            title: "Sales & Marketing Professionals Mixer",
            date: "April 2, 2024",
            summary: "Monthly networking events focused on relationship building and lead generation strategies.",
            location: `${location.includes("virtual") ? "Virtual Event" : "Business Networking Lounge"}`,
            demographics: { sales: 60, marketing: 40 }
        });
        
    } else {
        // Generic recommendations based on location
        events.push({
            title: `Professional Networking Association Meetup in ${location}`,
            date: "March 30, 2024",
            summary: "Regular events bringing together professionals from diverse backgrounds.",
            location: `${location.includes("virtual") ? "Virtual Event" : "Community Business Center"}`,
            demographics: { various: 50, business: 50 }
        });
        
        events.push({
            title: "Industry Insights Conference",
            date: "April 10, 2024",
            summary: `A major ${location.includes("virtual") ? "virtual" : "in-person"} event with keynote speakers and structured networking sessions.`,
            location: `${location.includes("virtual") ? "Virtual Event" : "Downtown Convention Center"}`,
            demographics: { business: 65, tech: 35 }
        });
    }
    
    // Universal recommendation - add to all results
    events.push({
        title: "Cross-Industry Networking Event",
        date: "April 18, 2024",
        summary: `Connect with professionals from various fields to expand your network beyond your immediate industry. ${location.includes("virtual") ? "Hosted virtually with breakout rooms for focused conversations." : "Features speed networking and open discussion forums."}`,
        location: `${location.includes("virtual") ? "Virtual Event" : "Grand Community Center"}`,
        demographics: { tech: 40, business: 30, creative: 30 }
    });
    
    return events;
}

// Store user profile in session storage before redirecting
function storeProfileAndRedirect() {
    // Make sure we have a userProfile object with data
    if (userProfile && userProfile.profession) {
        // Store the profile in sessionStorage
        sessionStorage.setItem('userProfile', JSON.stringify(userProfile));
        
        // Redirect to the relevant events page
        window.location.href = 'relevant-events.html';
    } else {
        console.error('No user profile available to store');
    }
}

// Function to populate relevant-events.html with event cards
function populateRelevantEvents() {
    // Get the container for event cards
    const eventCardsContainer = document.querySelector('.event-cards');
    
    // Make sure the container exists (we're on the relevant-events page)
    if (!eventCardsContainer) return;
    
    // Clear any existing cards
    eventCardsContainer.innerHTML = '';
    
    // Get events based on stored user profile
    const events = generateEventRecommendations();
    
    // Create and add each event card
    events.forEach(event => {
        // Create card element
        const card = document.createElement('a');
        card.href = 'results.html';
        card.classList.add('event-card');
        
        // Create demographics section
        const demographics = document.createElement('div');
        demographics.classList.add('demographics');
        
        // Add demographic items
        Object.entries(event.demographics).forEach(([key, value]) => {
            const demoItem = document.createElement('span');
            demoItem.classList.add('demo-item', `demo-${key.toLowerCase()}`);
            demoItem.textContent = `${key.charAt(0).toUpperCase() + key.slice(1)} ${value}%`;
            demographics.appendChild(demoItem);
        });
        
        // Create date element
        const dateElement = document.createElement('div');
        dateElement.classList.add('event-date');
        dateElement.textContent = event.date;
        
        // Create title element
        const titleElement = document.createElement('h2');
        titleElement.classList.add('event-title');
        titleElement.textContent = event.title;
        
        // Create summary element
        const summaryElement = document.createElement('p');
        summaryElement.classList.add('event-summary');
        summaryElement.textContent = event.summary;
        
        // Create location element
        const locationElement = document.createElement('div');
        locationElement.classList.add('event-location');
        locationElement.textContent = `📍 ${event.location}`;
        
        // Assemble the card
        card.appendChild(demographics);
        card.appendChild(dateElement);
        card.appendChild(titleElement);
        card.appendChild(summaryElement);
        card.appendChild(locationElement);
        
        // Add the card to the container
        eventCardsContainer.appendChild(card);
    });
    
    // Add CSS for any additional demo types if not already in the HTML
    addDemographicsStyles();
}

// Function to add CSS for any demographic types that might not be in the HTML
function addDemographicsStyles() {
    // Check if styles for these demographics already exist
    if (!document.querySelector('style#demographics-styles')) {
        const style = document.createElement('style');
        style.id = 'demographics-styles';
        style.textContent = `
            .demo-finance {
                background-color: #e8f5e9;
                color: #2e7d32;
            }
            
            .demo-business {
                background-color: #ede7f6;
                color: #512da8;
            }
            
            .demo-marketing {
                background-color: #fff3e0;
                color: #e65100;
            }
            
            .demo-sales {
                background-color: #e0f7fa;
                color: #00838f;
            }
            
            .demo-various, .demo-creative {
                background-color: #f5f5f5;
                color: #616161;
            }
        `;
        document.head.appendChild(style);
    }
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

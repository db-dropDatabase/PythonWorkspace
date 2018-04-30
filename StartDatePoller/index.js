/**
 * I don't like OSU's crappy web portals, and I especially don't like refreshing them repeatedly
 * This script is designed to update the START registration portal without refreshing the page
 * giving the user an edge over every other sucker who is still downloading angularjs for the umpentienth time
 * 
 * A little analysis of the OSU START portal shows polls to the URLs below when populating the event list
 * By polling these URLs ourselves, we can see if START registration is ready without reloadin the page
 * So the first step is spamming that URL until START is ready
 * 
 * Once we know the event should be in the list, we need reload the events without refreshing the page
 * To do this, we use the a behavior of the "search failed" box--once clicked to close, the events are
 * immediatly restocked
 * Assuming we are on this page at the start, we can simply activate this button with javascript and be on
 * our merry way
 * 
 * To get to this "search failed" screen from the events list:
 * 1. type in a search term into the "search by title" box and hit enter
 * 2. watch as the site slowly starts to dissolve into madness
 * 3. refresh the page
 */

//Constants
// the magical URL the OSU event portal uses to check for events
const URL = "https://xe.ucsadm.oregonstate.edu:8890/SelfServiceBannerGeneralEventManagement/ssb/events/eventsList?selectedMonth=6&selectedYear=2018";
//URL where we want to navigate to in order to execute the script
const TARGET_URL = "https://xe.ucsadm.oregonstate.edu:8890/SelfServiceBannerGeneralEventManagement/ssb/events#/search/";
//selector of the close window button of the "search failed" dialog
const CLOSE_WINDOW_SELECTOR = ".search-close-icon";
//how fast to poll
const POLL_MS = 100;

//error func
const error = (msg) => {
    alert(msg);
    throw msg;
}

//Preliminary checks
//check current url to matchin our target url
if(!window.location.href.includes(TARGET_URL)) error("Wrong URL! Did you follow the instructions?");
//check if our close window button exists and has a click function
const button = document.querySelector(CLOSE_WINDOW_SELECTOR);
if(!button) error("Close button for search dialog is not present! Did you follow the inscructions?");
if(!button.click) error("Click function does not exist! This is the developers problem");

//START (lol) polling that url like mad
const poll = () => {
    console.log("Polling...");
    return fetch(URL).then((response) => {
        if(!response.ok) error("Response not OK");
        return response.json();
    }).then((json) => {
        //if we get an emptey array, try again
        if(json && Array.isArray(json) && json.length === 0) setTimeout(poll, POLL_MS);
        //else close the window cuz we're good to go
        else {
            console.log("GOGOGO");
            button.click();
        }
    });
}
//go!
poll();
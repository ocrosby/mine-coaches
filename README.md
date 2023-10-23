# Mine Coaches

## Overview

### What do I need this thing to do?

At present I have access to an endpoint that lists college teams from the SoccerHub API.

For example:

GET http://184.73.139.41/api/v1/tds/college/teams/?division=di&gender=female

Will retrieve a JSON response containing all DI female soccer teams.  Each team has the
form:

```json
  {
    "name": "Austin Peay",
    "gender": "female",
    "division": "di",
    "conference_name": "ASUN",
    "conference_tds_id": "22",
    "conference_tds_url": "https://www.topdrawersoccer.com/college/conference/?genderId=&conferenceId=22&conferenceName=asun",
    "tds_id": "263",
    "tds_url": "https://www.topdrawersoccer.com/college-soccer/college-soccer-details/women/austin-peay/clgid-263"
  }
```

You will note the tds_url field.  This is the URL for the team on the TopDrawerSoccer website.

This is my starting point. The question is how do I get from here to a list of all the coaches for a specified team?

On that TopDrawerSoccer page most teams have a "Website link" button at the top right of the page that
is essentially an anchor referencing the atheltics page of the teams website.

For example Austin Peay's page has a link to their athletics page: 

http://www.letsgopeay.com/

When I navigate to that page I see a menu at the top allowing the user to select Teams, Tickets, Shop, NIL, Donate, ...

But down at the bottom of the page I can see a reference to [sidarmsports.com](https://sidearmsports.com/).

It appears that this company handles the athletics pages for a number of schools.  So I am trying to identify the
website urls that appear to use them to see if I can figure out a pattern for how to access Women's Soccer coaching
staff's contact information in a reliable way across their customers.  The same will have to be done for other 
companies that provide similar services for college athletics departments.

At present I am unaware of how many such companies there are and if each site they host is consistent enough to 
allow me to do what I'm trying to do but I'm going to start with this one and see where it leads me.


### What am I trying to do?

Answer: I need something that lists all contact information for a specified set of women's Soccer teams.

### Why is this so challenging?

Answer: Each team has different methods for listing information about their coaches.

### Are there any patterns?
Answer: Yes, it appears there are companies out there that provide canned services to athletics departments for providing these details.

### Can you identifier the patterns programmatically?

Answer: It might be a little hit and miss there requiring an iterative approach to probing the page that has the coaches on it for each school.

### For a given team how do I locate the page that contains that teams coaches?

Answer: Since all I have is the TopDrawerSoccer URL from the API's teams endpoint I could start by visiting the "Website Link" for each team from TopDrawer.


## Usage

To execute the main script run the following command:

```bash
python3 -m mine.main
```

This program has a long runtime as it executes a number of operation
and executes many requests to determine what it needs to. In order
to iterate quickly and dynamicaly figure out what is needed I have
to make it reentrant. This means that it can be paused and resumed
without unnecessarily duplicating work while it is doing what it does.

## Reentrancy

To make your program reentrant, you need to ensure that it can be paused and resumed without losing its current state. Here's a step-by-step guide on how to achieve reentrancy in your program:

1. **Identify Checkpoints**:
   Divide your long-running process into logical checkpoints or stages where you can save the current state. These checkpoints should represent parts of the process that can be paused and resumed without losing progress.

2. **Serialize State**:
   For each checkpoint, serialize the relevant state into a file or database. Serialization involves converting the current state (variables, data, and any other necessary information) into a format that can be saved and later deserialized.

3. **Deserialize State**:
   When resuming the program, read the serialized state from the storage location and deserialize it to restore the program to its previous state.

4. **Handle Dependencies**:
   Ensure that the program can handle any dependencies or changes that may have occurred between checkpoints. For example, if external data sources have changed, the program should account for this and reconcile any differences.

5. **Error Handling and Recovery**:
   Implement proper error handling and recovery mechanisms. If the program is interrupted due to an error or failure, it should be able to resume from a previous checkpoint. Handle exceptions and failures gracefully, and provide recovery options.

6. **Concurrency Considerations**:
   If your program involves concurrent execution, ensure that the reentrant approach is thread-safe and doesn't lead to data corruption. Use appropriate locks or synchronization mechanisms to manage concurrent access to shared resources.

7. **Testing and Validation**:
   Thoroughly test your reentrant program to ensure that it can be reliably paused and resumed without data loss or errors. Test different scenarios, including interruptions due to errors or external events.

8. **Documentation**:
   Document the reentrant functionality in your program, including how to pause and resume it, the supported checkpoints, and any special considerations for users or developers.

By following these steps, you can make your program reentrant, allowing you to pause and resume its execution without losing progress or data. This is especially useful for long-running processes and critical applications where interruptions can occur.


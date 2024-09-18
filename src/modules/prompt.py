import curses

def prompt(stdscr, collection_list, chosen_list, prompt_message, back):
    # Clear and refresh the screen
    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()

    # Copy the collection list of options
    collection_lst = collection_list[:] 

    if back == True:
        collection_lst.append('GO BACK')
    collection_lst.append('EXIT')

    # Initialize the current selected option to 0
    current_option = 0
    
    # Loop indefinitely until a selection is made
    while True:
        # Clear the screen
        stdscr.clear()
        
        # Display the prompt message at the top of the screen
        stdscr.addstr(prompt_message)
        # Display the chosen list separately
        stdscr.addstr(f"\nChosen: {chosen_list}\n", curses.A_DIM)
        
        # Iterate over each item in the collection_lst
        for idx, item in enumerate(collection_lst):
            try:
                # Highlight the currently selected option
                if idx == current_option:
                    stdscr.addstr(f"> {item}\n", curses.A_BOLD)
                else:
                    stdscr.addstr(f"  {item}\n")
            except curses.error:
                print('The terminal window might be so small')
                exit()
        # Refresh the screen to display changes
        stdscr.refresh()
        
        # Get the user's input (key press)
        key = stdscr.getch()

        # Handle navigation keys (up and down arrow keys)
        if key == curses.KEY_UP:
            current_option = (current_option - 1) % len(collection_lst)
        elif key == curses.KEY_DOWN:
            current_option = (current_option + 1) % len(collection_lst)
        # Handle selection (Enter key)
        elif key == 10:  # 'Enter' key
            # Return the selected option
            return collection_lst[current_option]
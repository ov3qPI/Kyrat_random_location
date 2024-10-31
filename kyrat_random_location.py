import random
import pandas as pd
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

# Load Kyrat Locations from CSV
import os
locations_df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'kyrat_locations_list.csv'), engine='python', delimiter=',')
# Ensure all columns are present for every row
expected_columns = locations_df.columns  # Assuming we want all columns consistently
locations_df = locations_df.reindex(columns=expected_columns, fill_value=None)

def generate_location(tags):
    # Filter locations based on provided tags
    filtered_locations = locations_df
    filtered_subset = pd.DataFrame()  # Initialize the DataFrame outside the loop
    if tags:
        import shlex
        tag_list = shlex.split(tags)  # Split tags by spaces, respecting quoted phrases  # Split tags by spaces to support multiple tag inputs
        or_tags = []  # To hold tags with '~' symbol
        for tag in tag_list:
            if '~' in tag:
                or_tags.append(tag.replace('~', ''))
            else:
                filtered_subset = pd.DataFrame()  # Reset filtered_subset for each tag
                tag_found = False
                negate = tag.startswith("-")
                actual_tag = tag[1:] if negate else tag
                for column in locations_df.columns:
                    if column.lower() != 'location':
                        if negate:
                            matches = filtered_locations[~filtered_locations[column].str.contains(actual_tag, case=False, na=False)]
                        else:
                            matches = filtered_locations[filtered_locations[column].astype(str).str.contains(actual_tag, case=False, na=False)]
                        if not matches.empty:
                            tag_found = True
                            filtered_subset = pd.concat([filtered_subset, matches])

                if not tag_found:
                    print(f"Tag '{tag}' not found")
                    return "No locations found with the given tags."

                filtered_locations = filtered_subset.drop_duplicates()
                if filtered_locations.empty:
                    break

        # Process '~' tags (OR condition)
        if or_tags:
            or_filtered_subset = pd.DataFrame()
            for or_tag in or_tags:
                for column in locations_df.columns:
                    if column.lower() != 'location':
                        matches = locations_df[locations_df[column].str.contains(or_tag, case=False, na=False)]
                        or_filtered_subset = pd.concat([or_filtered_subset, matches])
            if not or_filtered_subset.empty:
                filtered_locations = pd.concat([filtered_locations, or_filtered_subset]).drop_duplicates()

    if not filtered_locations.empty:
        selected_location = filtered_locations.sample().iloc[0]
        location_name = selected_location['Location']
        x_coord = selected_location.get('X', '?')
        y_coord = selected_location.get('Y', '?')
        x_coord = '?' if pd.isna(x_coord) else x_coord
        y_coord = '?' if pd.isna(y_coord) else y_coord

        # Check if the location is unmarked by searching all columns for the word 'unmarked'
        unmarked_tag = ""
        for value in selected_location:
            if isinstance(value, str) and 'unmarked' in value:
                unmarked_tag = " (unmarked)"
                break

        return f"{location_name}, X:{x_coord}, Y:{y_coord}{unmarked_tag}"
    else:
        return "No locations found with the given tags."

def main():
    # Collect all unique values across relevant columns for autocompletion
    unique_values = set()
    for column in locations_df.columns:
        if column.lower() != 'location':
            unique_values.update(locations_df[column].dropna().unique().tolist())

    completer = WordCompleter([str(value) for value in unique_values], ignore_case=True)

    print("Enter tags to filter locations (you can enter anything, or press Enter to skip):")
    tags = prompt("Tags: ", completer=completer).strip()

    location = generate_location(tags)
    print(location)

if __name__ == "__main__":
    main()

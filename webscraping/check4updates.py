# %%
def check():
    import getDatabaseDate

    with open('./outputs/database_date.txt', 'r') as f:
        date = f.readlines()[0].strip()

    janus_date = getDatabaseDate.dateGetter()

    # check for updates
    if date == janus_date:
        print('No updates needed B)')
    else:
        print('Update databse needed !!')

# %%

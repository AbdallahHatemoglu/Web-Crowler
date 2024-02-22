import os


# This function will create a folder for each website we
# crawl, and if the website exists it will not create a new
# folder for it.
# Each website we crawl is a separate project (folder)
def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating directory ' + directory)
        os.makedirs(directory)


# for each website we crawl, we will have only two files
# the queue and the crawled files, and inside them will be the links
# Create queue and crawled files (if not created)
def create_data_files(project_name, base_url):
    queue = os.path.join(project_name, 'queue.txt')
    crawled = os.path.join(project_name, "crawled.txt")

    if not os.path.isfile(queue):
        write_file(queue, base_url)
        # whenever we make this crawled file we want to make it is an empty file
        # and that is because if we just go and make it and throw URL in there
        # then our program is going to think that we crawled this already,
        # but we just created the file, so we obviously did not crawl this page yet
        # and again later what is going to happen is we are going to go ahead and look at
        # the waiting list crawl the homepage and after we crawling it then we move it to crawled
    if not os.path.isfile(crawled):
        write_file(crawled, '')


# create a new file
def write_file(path, data):
    with open(path, 'w') as f:
        f.write(data)


# Adding data onto an existing file
def append_to_file(path, data):
    with open(path, 'a') as file:
        file.write(data + '\n')


# Delete the contents of a file
def delete_file_contents(path):
    open(path, 'w').close()


# so if a file exists instead of just reading through every line
# and deleting it one by one we are just going to create a file
# with the same name and that is essentially just going to delete
# all the contents in it.


# Read a file and convert each line to set items
def file_to_set(file_name):
    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results


# Iterate through a set, each item will be a new line in the file
def set_to_file(links, file_name):
    with open(file_name, "w") as f:
        for l in sorted(links):
            f.write(l + "\n")

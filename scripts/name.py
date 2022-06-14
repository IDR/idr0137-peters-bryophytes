import omero.cli
import omero.gateway
import pandas
import os


project_id = 2402
anno_file = "/uod/idr/metadata/idr0137-peters-bryophytes/experimentA/idr0137-riccia-annotation.csv"


def image_names_csv(file):
    image_names = {}
    df = pandas.read_csv(file, dtype=str)
    for index, row in df.iterrows():
        filename = row["Image File"]
        image_names[os.path.splitext(filename)[0]] = filename
    return image_names


def image_names_imported(project):
    image_names = {}
    for dataset in project.listChildren():
        for image in dataset.listChildren():
            filename = image.getName()
            image_names[filename.replace('.ome.tiff', '').strip()] = filename
    return image_names


if __name__ == "__main__":
    with omero.cli.cli_login() as c:
        images_csv = image_names_csv(anno_file)

        conn = omero.gateway.BlitzGateway(client_obj=c.get_client())
        project = conn.getObject("Project", attributes={'id': project_id})
        images_imported = image_names_imported(project)

        print("Check CSV:")
        for image, filename in images_csv.items():
            if image in images_imported:
                print(f"{filename} -> {images_imported[image]}")
            else:
                print(f"{filename} -> NO IMAGE")

        print("Check IMPORTED:")
        for image, filename in images_imported.items():
            if image not in images_csv:
                print(f"{filename} -> NOT IN CSV")

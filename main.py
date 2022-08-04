from discord_dumper.extractor import parse_records, write_to_separate_dbs

recs = parse_records("data/spazdicknt_dump.csv")

write_to_separate_dbs("output/partners", recs)
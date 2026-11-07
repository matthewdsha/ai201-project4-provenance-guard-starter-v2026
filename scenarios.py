"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.
"""

SCENARIOS = [
    {
        # Criterion 1. Ten human-written paragraphs; the FIRST FOUR are the
        # deliberately plain ones (short sentences, common words, the way a
        # second-language writer might write). The grader treats texts 1-4 as plain.
        "name": "false positives",
        "criterion": 1,
        "texts": ['I get up at six every day. I make tea and I sit by the window. My street is quiet in the '
 'morning. A man walks his dog past my house at the same time each day. I like this part of the '
 'day best. After tea I take the bus to work. The bus is often late. I read a book on the bus and '
 'the time goes fast.',
 'Last year I started a new job in a new city. At first I was afraid. I did not know anyone and my '
 'English was not good. My manager was patient with me. She spoke slowly and she wrote things '
 'down. Now I understand most of what people say. I still make mistakes, but I am not afraid any '
 'more.',
 'My sister has a small shop that sells fruit. She opens it at eight and closes it at six. She '
 'works six days a week. On Sundays she rests and she cooks for the family. I help her in the shop '
 'when I am not at school. I have learned how to count money and how to speak to customers. I '
 'think this will help me later.',
 'The park near my school has a big lake. In summer many people come there to walk and to sit. '
 'Children feed the ducks with bread. There is also a small cafe that sells ice cream. In winter '
 'the lake gets very cold and sometimes it freezes. Then the park is empty and very quiet. I like '
 'it more in winter.',
 "Honestly the worst part of moving flat wasn't the boxes, it was finding out at 11pm that the "
 "kettle was in the box marked 'books'. My brother swears he packed it right. He did not. We drank "
 'cold coffee out of a measuring jug and argued about whose fault it was until the neighbour '
 'banged on the wall.',
 "I've been learning to bake bread for about a year now and I still can't get the crumb right. "
 "Mine comes out dense, like a brick with ambitions. Gran says it's the flour. My flatmate says I "
 'knead it wrong. I think the oven in this place just hates me, because it burns the left side '
 'every single time.',
 "We drove up to Whitby in my dad's ancient Volvo, which smells permanently of wet dog even though "
 "we haven't owned a dog since 2014. Rained the whole way. The chips were great though, eaten in "
 'the car with the windows steamed up, watching a seagull stare down a man holding a sausage roll.',
 'Not gonna lie, I almost quit the choir twice this term. Rehearsals run late, the hall is '
 "freezing, and Margaret keeps correcting my breathing like she's training a racehorse. But then "
 'we nailed the Fauré on Thursday and the whole room went quiet for a second and I got that '
 'tingle. So. Still here.',
 'My grandfather kept bees behind the garage and never wore a veil, which my mum says is how he '
 'got that scar on his ear. He used to hum to them. I thought it was nonsense until the summer I '
 "tried it and a whole hive calmed down in front of me. I still don't understand it.",
 "Tuesday I missed the train because I went back for my umbrella, and it didn't even rain. Then "
 'the next train was cancelled, so I walked the long way past the canal, and found a tiny '
 "second-hand bookshop I'd somehow never noticed in four years of living here. Bought three books. "
 'Late for work. Worth it.'],
    },
    {
        # Criterion 2. Same AI paragraph and same personal-voice paragraph in
        # every trial: the gap between their combined scores is what is checked.
        "name": "score spread",
        "criterion": 2,
        "texts": [
            ('Effective communication is a cornerstone of successful teamwork in any modern workplace. When '
 'team members share information clearly and listen actively to one another, they are better '
 'positioned to align on goals, avoid misunderstandings, and respond quickly to challenges. '
 'Furthermore, regular check-ins and transparent documentation foster a culture of trust and '
 'accountability. By prioritizing open dialogue, organizations can enhance collaboration, improve '
 'productivity, and ultimately achieve their strategic objectives.'),
            ("I'll be honest, the team meeting yesterday was a mess. Priya turned up twenty minutes late with "
 "a coffee she'd clearly bought on the way, Tom kept sharing the wrong screen, and somehow we "
 'ended up arguing about the office fridge for ten minutes instead of the Q3 plan. Still, '
 'afterwards three of us went for chips and actually sorted the budget thing out, which is more '
 'than the meeting managed.'),
        ],
    },
    {
        # Criterion 3. In this order: clearly AI, clearly human, plainly written
        # human, lightly edited AI (a few words swapped).
        "name": "label coverage",
        "criterion": 3,
        "texts": [
            ('Effective communication is a cornerstone of successful teamwork in any modern workplace. When '
 'team members share information clearly and listen actively to one another, they are better '
 'positioned to align on goals, avoid misunderstandings, and respond quickly to challenges. '
 'Furthermore, regular check-ins and transparent documentation foster a culture of trust and '
 'accountability. By prioritizing open dialogue, organizations can enhance collaboration, improve '
 'productivity, and ultimately achieve their strategic objectives.'),
            ("I'll be honest, the team meeting yesterday was a mess. Priya turned up twenty minutes late with "
 "a coffee she'd clearly bought on the way, Tom kept sharing the wrong screen, and somehow we "
 'ended up arguing about the office fridge for ten minutes instead of the Q3 plan. Still, '
 'afterwards three of us went for chips and actually sorted the budget thing out, which is more '
 'than the meeting managed.'),
            ('Last year I started a new job in a new city. At first I was afraid. I did not know anyone and my '
 'English was not good. My manager was patient with me. She spoke slowly and she wrote things '
 'down. Now I understand most of what people say. I still make mistakes, but I am not afraid any '
 'more.'),
            ('Good communication is a cornerstone of successful teamwork in any modern office. When team '
 'members share information clearly and listen closely to one another, they are better placed to '
 'agree on goals, avoid mix-ups, and react quickly to problems. Also, regular check-ins and open '
 'documentation build a culture of trust and responsibility. By putting open dialogue first, '
 'companies can improve collaboration, raise productivity, and in the end reach their strategic '
 'goals.'),
        ],
    },

    # Criterion 4 (appeal path) and criterion 5 (bad input) cannot be expressed
    # here: an appeal needs a content_id from a earlier submit, and criterion 5
    # needs a JSON list body and invalid JSON, but "bodies" only holds dicts. I
    # extended the harness instead: see run_eval_extra.py.
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems

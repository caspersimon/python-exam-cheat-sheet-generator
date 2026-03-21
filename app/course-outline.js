const COURSE_OUTLINE = [
  {
    id: "week-1",
    week: 1,
    title: "Week 1",
    groups: [
      {
        id: "week-1-basics",
        shortTitle: "Python Basics",
        title: "Introduction to Python: Python Basics",
        matchers: [
          /\bvariables?\b/i,
          /\blogic\b/i,
          /\bbooleans?\b/i,
          /\bcomparison\b/i,
          /\barithmetic\b/i,
          /\bassignment\b/i,
          /\bconversion\b/i,
          /\bimmutable\b/i,
          /\bobjects?\b/i,
          /\bidentity\b/i,
          /\bexecution model\b/i,
          /\bnaming rule\b/i,
          /\bdata basics\b/i,
          /\bexam question types\b/i,
          /\bknow object\b/i,
        ],
      },
      {
        id: "week-1-lists",
        shortTitle: "Python Lists",
        title: "Introduction to Python: Python Lists",
        matchers: [
          /\blists?\b/i,
          /\btuples?\b/i,
          /\bindexing\b/i,
          /\bslicing\b/i,
          /\bappend\b/i,
          /\bextend\b/i,
          /\bsingle element tuple\b/i,
        ],
      },
      {
        id: "week-1-functions-packages",
        shortTitle: "Functions and Packages",
        title: "Introduction to Python: Functions and Packages",
        matchers: [
          /\bbuilt[ -]?in functions?\b/i,
          /\bimporting package\b/i,
          /\bpackages?\b/i,
          /\bmodules?\b/i,
        ],
      },
      {
        id: "week-1-related",
        shortTitle: "Related Foundations",
        title: "Related Foundations and Carry-Over",
        fallback: true,
        matchers: [],
      },
    ],
  },
  {
    id: "week-2",
    week: 2,
    title: "Week 2",
    groups: [
      {
        id: "week-2-dictionaries",
        shortTitle: "Dictionaries",
        title: "Intermediate Python: Dictionaries",
        matchers: [
          /\bdictionaries\b/i,
          /\bdictionary\b/i,
          /\bdict\b/i,
          /\bsets?\b/i,
        ],
      },
      {
        id: "week-2-logic-control",
        shortTitle: "Logic and Filtering",
        title: "Intermediate Python: Logic, Control Flow and Filtering",
        matchers: [
          /\btruthy\b/i,
          /\bfalsy\b/i,
          /\bconditional\b/i,
          /\bternary\b/i,
          /\bwalrus\b/i,
          /\bzip\b/i,
          /\benumerate\b/i,
          /\bprecedence\b/i,
        ],
      },
      {
        id: "week-2-loops",
        shortTitle: "Loops",
        title: "Intermediate Python: Loops",
        matchers: [
          /\bloops?\b/i,
          /\bwhile\b/i,
          /\brange\b/i,
        ],
      },
      {
        id: "week-2-related",
        shortTitle: "Related Practice",
        title: "Related Practice and Carry-Over",
        fallback: true,
        matchers: [],
      },
    ],
  },
  {
    id: "week-3",
    week: 3,
    title: "Week 3",
    groups: [
      {
        id: "week-3-writing-functions",
        shortTitle: "Writing Functions",
        title: "Introductions to Functions in Python: Writing your own functions",
        matchers: [
          /\bfunction definition\b/i,
          /\bfunctions and methods\b/i,
          /\breturn values?\b/i,
          /\bnone returns?\b/i,
          /\bimplicit none return\b/i,
          /\bglobals and none returns?\b/i,
        ],
      },
      {
        id: "week-3-args-scope",
        shortTitle: "Arguments and Scope",
        title: "Introductions to Functions in Python: Default arguments, variable-length arguments and scope",
        matchers: [
          /\*args/i,
          /\*\*kwargs/i,
          /\barguments?\b/i,
          /\bkeyword arguments?\b/i,
          /\bdefault arguments?\b/i,
          /\bdefault args?\b/i,
          /\bscope\b/i,
          /\bglobal vs local\b/i,
          /\bunboundlocal/i,
          /\bunpacking\b/i,
          /\bmutable args?\b/i,
        ],
      },
      {
        id: "week-3-lambda-errors",
        shortTitle: "Lambda and Errors",
        title: "Introductions to Functions in Python: Lambda functions and error handling",
        matchers: [
          /\blambda\b/i,
          /\bmap\b/i,
          /\bfilter\b/i,
          /\breduce\b/i,
          /\bfactor(?:y|ies)\b/i,
          /\bclosures?\b/i,
          /\berror handling\b/i,
          /\braise keyword\b/i,
          /\bkey sorted\b/i,
        ],
      },
      {
        id: "week-3-related",
        shortTitle: "Related Function Topics",
        title: "Related Function Topics and Carry-Over",
        fallback: true,
        matchers: [],
      },
    ],
  },
  {
    id: "week-4",
    week: 4,
    title: "Week 4",
    groups: [
      {
        id: "week-4-string-basics",
        shortTitle: "String Manipulation",
        title: "Regular Expressions in Python: Basic Concepts of String Manipulation",
        matchers: [
          /\bstrings?\b/i,
          /\bstripping\b/i,
          /\bsearching\b/i,
          /\bescape\b/i,
          /\bjoin\b/i,
          /\breplace method\b/i,
          /\bstring immutability\b/i,
        ],
      },
      {
        id: "week-4-string-formatting",
        shortTitle: "Formatting Strings",
        title: "Regular Expressions in Python: Formatting Strings",
        matchers: [
          /\bf[ -]?strings?\b/i,
          /\bstring formatting\b/i,
          /\bformatting strings?\b/i,
          /\bformatting in while loops\b/i,
        ],
      },
      {
        id: "week-4-oop",
        shortTitle: "OOP Fundamentals",
        title: "Object-Oriented Programming in Python: OOP Fundamentals",
        matchers: [
          /\boop\b/i,
          /\bclass definition\b/i,
          /\bself parameter\b/i,
          /\binstance attributes?\b/i,
          /\binitializer\b/i,
        ],
      },
      {
        id: "week-4-related",
        shortTitle: "Related Week 4 Topics",
        title: "Related Week 4 Topics and Carry-Over",
        fallback: true,
        matchers: [],
      },
    ],
  },
  {
    id: "week-5",
    week: 5,
    title: "Week 5",
    groups: [
      {
        id: "week-5-loading-pandas",
        shortTitle: "Loading Data in pandas",
        title: "Introduction to Data Science in Python: Loading Data in pandas",
        matchers: [
          /\bpandas basics\b/i,
          /\bdataframes?\b/i,
          /\bviewing data\b/i,
          /\bmissing data\b/i,
          /\bpd[ .]?series\b/i,
        ],
      },
      {
        id: "week-5-pandas-operations",
        shortTitle: "pandas Operations",
        title: "10 Minutes to pandas: Operations",
        matchers: [
          /\bpandas\b/i,
          /\bloc\b/i,
          /\biloc\b/i,
          /\bsubsetting\b/i,
          /\bsorting\b/i,
          /\bgrouping\b/i,
          /\bmerging\b/i,
          /\bapply\b/i,
          /\bbroadcasting\b/i,
          /\bconcatenation\b/i,
          /\bdatetimeindex\b/i,
          /\bboolean indexing\b/i,
          /\bvectorized string\b/i,
          /\bisin\b/i,
          /\bselection\b/i,
        ],
      },
      {
        id: "week-5-related",
        shortTitle: "Related pandas Topics",
        title: "Related pandas Topics and Carry-Over",
        fallback: true,
        matchers: [],
      },
    ],
  },
  {
    id: "week-6",
    week: 6,
    title: "Week 6",
    groups: [
      {
        id: "week-6-iterators",
        shortTitle: "Iterators",
        title: "Python Toolbox: Using iterators in PythonLand",
        matchers: [
          /\biterators?\b/i,
          /\biterables?\b/i,
        ],
      },
      {
        id: "week-6-comprehensions",
        shortTitle: "Comprehensions and Generators",
        title: "Python Toolbox: List comprehensions and generators",
        matchers: [
          /\bcomprehensions?\b/i,
          /\bgenerators?\b/i,
          /\bstring list transformations?\b/i,
        ],
      },
      {
        id: "week-6-dates-times",
        shortTitle: "Dates and Times",
        title: "Working with Dates and Times in Python",
        matchers: [
          /\bdatetime\b/i,
          /\bdate formatting\b/i,
          /\bdate parsing\b/i,
          /\bstrftime\b/i,
          /\bstrptime\b/i,
          /\btimedeltas?\b/i,
          /\btimestamps?\b/i,
          /\bdates? and times?\b/i,
        ],
      },
      {
        id: "week-6-related",
        shortTitle: "Related Week 6 Topics",
        title: "Related Week 6 Topics and Carry-Over",
        fallback: true,
        matchers: [],
      },
    ],
  },
];

const COURSE_GROUP_LOOKUP = new Map(
  COURSE_OUTLINE.flatMap((weekConfig) =>
    (weekConfig.groups || []).map((group) => [
      group.id,
      {
        week: weekConfig.week,
        weekTitle: weekConfig.title,
        group,
      },
    ])
  )
);

const COURSE_GROUP_MATCH_ORDER = [
  "week-5-loading-pandas",
  "week-5-pandas-operations",
  "week-6-iterators",
  "week-6-comprehensions",
  "week-6-dates-times",
  "week-4-oop",
  "week-4-string-formatting",
  "week-4-string-basics",
  "week-3-args-scope",
  "week-3-lambda-errors",
  "week-3-writing-functions",
  "week-2-dictionaries",
  "week-2-logic-control",
  "week-2-loops",
  "week-1-lists",
  "week-1-functions-packages",
  "week-1-basics",
];

function normalizeCourseOutlineText(value) {
  return String(value || "")
    .toLowerCase()
    .replace(/&/g, " and ")
    .replace(/[^a-z0-9*+. ]+/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function getCourseMatchText(card) {
  const pieces = [
    card?.topic,
    card?.canonical_topic,
  ];
  return normalizeCourseOutlineText(pieces.join(" "));
}

function getCourseOutlineWeek(week) {
  return COURSE_OUTLINE.find((entry) => entry.week === Number(week)) || null;
}

function getCourseFallbackWeek(card) {
  const weightedWeeks = new Map();
  const addWeight = (week, amount) => {
    if (!Number.isFinite(week)) {
      return;
    }
    weightedWeeks.set(week, (weightedWeeks.get(week) || 0) + amount);
  };

  (card?.sections?.lecture_snippets || []).forEach((item) => addWeight(Number(item?.week), 3));
  (card?.sections?.notebook_snippets || []).forEach((item) => addWeight(Number(item?.week), 1));

  if (weightedWeeks.size > 0) {
    return [...weightedWeeks.entries()].sort((a, b) => {
      const weightDelta = b[1] - a[1];
      if (weightDelta !== 0) {
        return weightDelta;
      }
      return a[0] - b[0];
    })[0][0];
  }

  const cardWeeks = (card?.weeks || []).filter((week) => Number.isFinite(Number(week))).map(Number);
  if (cardWeeks.length > 0) {
    return Math.min(...cardWeeks);
  }

  return COURSE_OUTLINE[0].week;
}

function matchesCourseGroup(text, group) {
  return (group.matchers || []).some((matcher) => matcher.test(text));
}

function getCoursePlacement(card) {
  const text = getCourseMatchText(card);

  for (const groupId of COURSE_GROUP_MATCH_ORDER) {
    const entry = COURSE_GROUP_LOOKUP.get(groupId);
    if (!entry || entry.group.fallback || !matchesCourseGroup(text, entry.group)) {
      continue;
    }

    return {
      week: entry.week,
      weekTitle: entry.weekTitle,
      groupId: entry.group.id,
      groupTitle: entry.group.title,
      groupShortTitle: entry.group.shortTitle || entry.group.title,
      isFallback: false,
    };
  }

  const fallbackWeek = getCourseFallbackWeek(card);
  const weekConfig = getCourseOutlineWeek(fallbackWeek) || COURSE_OUTLINE[0];
  const fallbackGroup = weekConfig.groups.find((group) => group.fallback) || weekConfig.groups[weekConfig.groups.length - 1];

  return {
    week: weekConfig.week,
    weekTitle: weekConfig.title,
    groupId: fallbackGroup.id,
    groupTitle: fallbackGroup.title,
    groupShortTitle: fallbackGroup.shortTitle || fallbackGroup.title,
    isFallback: true,
  };
}

(function(global) {
  "use strict";

  // track how many times each entry point has run
  var runcount = {
    jsfuzzer: 0,
    eventhandler1: 0,
    eventhandler2: 0,
    eventhandler3: 0,
    eventhandler4: 0,
    eventhandler5: 0
  };

  // try to force garbage collection (IE & Node with --expose-gc)
  function freememory() {
    try { CollectGarbage(); } catch(e) {}
    try { global.gc(); } catch(e) {}
  }

  // small var-store helpers
  function GetVariable(store, type) {
    return store[type] || null;
  }
  function SetVariable(store, name, type) {
    store[type] = name;
  }

  // main fuzz entry
  function jsfuzzer() {
    runcount.jsfuzzer++;
    if (runcount.jsfuzzer > 2) return;
    /*<jsfuzzer>*/
  }

  // additional “event” fuzzers
  function eventhandler1() {
    runcount.eventhandler1++;
    if (runcount.eventhandler1 > 2) return;
    /*<jsfuzzer>*/
  }
  function eventhandler2() {
    runcount.eventhandler2++;
    if (runcount.eventhandler2 > 2) return;
    /*<jsfuzzer>*/
  }
  function eventhandler3() {
    runcount.eventhandler3++;
    if (runcount.eventhandler3 > 2) return;
    /*<jsfuzzer>*/
  }
  function eventhandler4() {
    runcount.eventhandler4++;
    if (runcount.eventhandler4 > 2) return;
    /*<jsfuzzer>*/
  }
  function eventhandler5() {
    runcount.eventhandler5++;
    if (runcount.eventhandler5 > 2) return;
    /*<jsfuzzer>*/
  }

  // expose APIs if you want, e.g. for external triggering:
  global.jsfuzzer       = jsfuzzer;
  global.eventhandler1  = eventhandler1;
  global.eventhandler2  = eventhandler2;
  global.eventhandler3  = eventhandler3;
  global.eventhandler4  = eventhandler4;
  global.eventhandler5  = eventhandler5;
  global.GetVariable    = GetVariable;
  global.SetVariable    = SetVariable;
  global.freememory     = freememory;

  // automatically invoke all of them once on load
  jsfuzzer();
  eventhandler1();
  eventhandler2();
  eventhandler3();
  eventhandler4();
  eventhandler5();

})(typeof window !== "undefined" ? window : global);

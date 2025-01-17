
# Value Strategies

Import from `controlsurfaces.valuestrategy`

Value strategies are used to get the value from an event and convert it to a
floating point value for use within the rest of the script.

## `IValueStrategy`

The interface used by all value strategies. If none of the following strategies
match your requirements, you can make a custom strategy by implementing this.
Note that value strategies should be stateless.

### Functions to Implement

* `getValueFromEvent(self, event: eventData) -> T`: Returns a value for internal
  use with this strategy, given a MIDI event.
* `getChannelFromEvent(self, event: EventData) -> int`: Returns the channel
  that the event is associated with, or -1 for no channel.
* `getValueFromFloat(self, f: float) -> T`: Returns a value for internal use
  with this strategy, given a float between 0 and 1.
* `getFloatFromValue(self, value: T) -> float`: Returns a float between 0 and 1
  given the internal value of this strategy.

## `Data2Strategy`

Gets the value from the data2 value of the event. Most standard events can use
this strategy.

## `Data1Strategy`

Gets the value from the data1 value of the event. This is used by some events
such as channel aftertouch which don't give a data2 value.

## `ButtonData2Strategy`

The same as the `Data2Strategy`, but only allowing press (127 -> 1.0) and
release (0 -> 0.0) values. Used for some button types.

## `ButtonSinglePressStrategy`

Used for buttons which only send an event when they are pressed.

## `NullStrategy`

Used by `NullEvents`. Has no meaningful value.

## `ForwardedStrategy`

Used to get values from forwarded events. Another value strategy should be
provided to the constructor.

## `ForwardedUnionStrategy`

Used to get values from events that can be either forwarded or not. If an event
is forwarded, a `ForwardedStrategy` will be used. Otherwise, the standard
strategy will be used. Another value strategy should be provided to the
constructor.

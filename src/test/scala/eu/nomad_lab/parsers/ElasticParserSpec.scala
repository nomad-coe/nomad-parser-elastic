package eu.nomad_lab.parsers

import org.specs2.mutable.Specification

object ElasticParserSpec extends Specification {

  "ElasticParserTestSpin" >> {
    "test with json-events" >> {
      ParserRun.parse(ElasticParser, "parsers/elastic/test/examples/elastic/INFO.OUT", "json-events") must_== ParseResult.ParseSuccess
    }
    "test with json" >> {
      ParserRun.parse(ElasticParser, "parsers/elastic/test/examples/elastic/INFO.OUT", "json") must_== ParseResult.ParseSuccess
    }

  }

}
